from typing import TypedDict, Annotated, Optional
import operator


class SearchResult(TypedDict):
    title: str
    url: str
    content: str
    source: str


class ArchiveResult(TypedDict):
    title: str
    content: str
    date: str
    relevance_score: float


class ConflictFlag(TypedDict):
    claim_a: str
    claim_b: str
    source_a: str
    source_b: str

# LangGraph works by passing a single state object through every node in the graph. 
# Each node reads from it and writes back to it. This class defines every field that state can have.
class AgentState(TypedDict):
    # Input
    topic: str

    # Accumulated across nodes
    search_results: Annotated[list[SearchResult], operator.add]
    archive_results: Annotated[list[ArchiveResult], operator.add]

    # Synthesized output
    briefing: Optional[str]
    sources: list[str]
    conflict_flags: Annotated[list[ConflictFlag], operator.add]

    # Routing
    needs_human_review: bool
    human_review_notes: Optional[str]

    # Metadata
    error: Optional[str]