from langgraph.graph import StateGraph, END

from .state import AgentState
from .node import search_node, retrieve_node, synthesize_node, human_review_node


def route_after_synthesize(state: AgentState) -> str:
    if state.get("needs_human_review"):
        return "human_review"
    return END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("search", search_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("human_review", human_review_node)

    graph.set_entry_point("search")
    graph.add_edge("search", "retrieve")
    graph.add_edge("retrieve", "synthesize")
    graph.add_conditional_edges(
        "synthesize",
        route_after_synthesize,
        {
            "human_review": "human_review",
            END: END,
        },
    )
    graph.add_edge("human_review", END)

    return graph.compile()


agent_graph = build_graph()