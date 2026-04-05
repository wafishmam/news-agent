import time
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ...agents.graph import agent_graph
from ...agents.state import ConflictFlag

logger = logging.getLogger(__name__)
router = APIRouter()


class BriefingRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=300)


class BriefingResponse(BaseModel):
    topic: str
    briefing: str
    sources: list[str]
    conflict_flags: list[ConflictFlag]
    needs_human_review: bool
    human_review_notes: Optional[str]
    latency_ms: int
    error: Optional[str] = None


@router.post("/briefing", response_model=BriefingResponse)
async def create_briefing(request: BriefingRequest) -> BriefingResponse:
    logger.info(f"Received briefing request: {request.topic!r}")
    start = time.monotonic()

    initial_state = {
        "topic": request.topic,
        "search_results": [],
        "archive_results": [],
        "briefing": None,
        "sources": [],
        "conflict_flags": [],
        "needs_human_review": False,
        "human_review_notes": None,
        "error": None,
    }

    try:
        final_state = await agent_graph.ainvoke(initial_state)
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    latency_ms = int((time.monotonic() - start) * 1000)

    return BriefingResponse(
        topic=request.topic,
        briefing=final_state.get("briefing") or "",
        sources=final_state.get("sources") or [],
        conflict_flags=final_state.get("conflict_flags") or [],
        needs_human_review=final_state.get("needs_human_review") or False,
        human_review_notes=final_state.get("human_review_notes"),
        latency_ms=latency_ms,
        error=final_state.get("error"),
    )