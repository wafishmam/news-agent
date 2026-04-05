import os
import json
import logging
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient

from .state import AgentState, SearchResult, ConflictFlag
from ..db.retriever import retrieve_archive

logger = logging.getLogger(__name__)


def get_llm() -> ChatAnthropic:
    return ChatAnthropic(
        model="claude-sonnet-4-5",
        temperature=0.2,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )


# ---------------------------------------------------------------------------
# Node: search
# ---------------------------------------------------------------------------

def search_node(state: AgentState) -> dict[str, Any]:
    logger.info(f"[search] Searching for: {state['topic']}")
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(
            query=state["topic"],
            search_depth="advanced",
            max_results=5,
        )
        results: list[SearchResult] = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
                "source": r.get("url", ""),
            }
            for r in response.get("results", [])
        ]
        logger.info(f"[search] Found {len(results)} results")
        return {"search_results": results, "error": None}
    except Exception as e:
        logger.error(f"[search] Error: {e}")
        return {"search_results": [], "error": str(e)}


# ---------------------------------------------------------------------------
# Node: retrieve
# ---------------------------------------------------------------------------

def retrieve_node(state: AgentState) -> dict[str, Any]:
    logger.info(f"[retrieve] Querying archive for: {state['topic']}")
    try:
        archive_results = retrieve_archive(query=state["topic"], k=5)
        logger.info(f"[retrieve] Found {len(archive_results)} archive matches")
        return {"archive_results": archive_results, "error": None}
    except Exception as e:
        logger.error(f"[retrieve] Error: {e}")
        return {"archive_results": [], "error": str(e)}


# ---------------------------------------------------------------------------
# Node: synthesize
# ---------------------------------------------------------------------------

SYNTHESIZE_SYSTEM_PROMPT = """You are a senior news researcher and editorial assistant.

Given a news topic and a set of source articles (both live and archived), your job is to:
1. Draft a structured editorial briefing of 3-5 paragraphs
2. Identify any conflicting claims between sources
3. List all sources used

Respond ONLY with valid JSON in this exact shape:
{
  "briefing": "...",
  "sources": ["url1", "url2"],
  "conflicts": [
    {
      "claim_a": "...",
      "claim_b": "...",
      "source_a": "url or title",
      "source_b": "url or title"
    }
  ]
}"""


def synthesize_node(state: AgentState) -> dict[str, Any]:
    logger.info("[synthesize] Drafting editorial briefing")
    llm = get_llm()

    context_parts = []
    for r in state.get("search_results", []):
        context_parts.append(
            f"[LIVE] {r['title']}\nSource: {r['url']}\n{r['content'][:800]}"
        )
    for r in state.get("archive_results", []):
        context_parts.append(
            f"[ARCHIVE] {r['title']} ({r['date']})\n{r['content'][:800]}"
        )

    context = "\n\n---\n\n".join(context_parts) if context_parts else "No source material found."
    user_message = f"Topic: {state['topic']}\n\nSources:\n\n{context}"

    try:
        response = llm.invoke([
            SystemMessage(content=SYNTHESIZE_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ])

        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        parsed = json.loads(raw)
        conflicts: list[ConflictFlag] = parsed.get("conflicts", [])

        return {
            "briefing": parsed.get("briefing", ""),
            "sources": parsed.get("sources", []),
            "conflict_flags": conflicts,
            "needs_human_review": len(conflicts) > 0,
            "error": None,
        }
    except Exception as e:
        logger.error(f"[synthesize] Error: {e}")
        return {
            "briefing": "Error generating briefing.",
            "sources": [],
            "conflict_flags": [],
            "needs_human_review": False,
            "error": str(e),
        }


# ---------------------------------------------------------------------------
# Node: human_review
# ---------------------------------------------------------------------------

def human_review_node(state: AgentState) -> dict[str, Any]:
    logger.info("[human_review] Formatting conflict flags for review")
    flags = state.get("conflict_flags", [])
    if not flags:
        return {"human_review_notes": None}

    lines = ["The following conflicting claims require editorial review:\n"]
    for i, flag in enumerate(flags, 1):
        lines.append(
            f"{i}. CONFLICT\n"
            f"   Claim A ({flag['source_a']}): {flag['claim_a']}\n"
            f"   Claim B ({flag['source_b']}): {flag['claim_b']}\n"
        )

    return {"human_review_notes": "\n".join(lines)}