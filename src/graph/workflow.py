from langgraph.graph import (
    StateGraph,
    END
)

from src.graph.state import (
    ResearchState
)

from src.graph.nodes import (
    search_node,
    reader_node,
    writer_node,
    critic_node
)


workflow = StateGraph(
    ResearchState
)


# NODES

workflow.add_node(
    "search_node",
    search_node
)

workflow.add_node(
    "reader_node",
    reader_node
)

workflow.add_node(
    "writer_node",
    writer_node
)

workflow.add_node(
    "critic_node",
    critic_node
)


# FLOW

workflow.set_entry_point(
    "search_node"
)

workflow.add_edge(
    "search_node",
    "reader_node"
)

workflow.add_edge(
    "reader_node",
    "writer_node"
)

workflow.add_edge(
    "writer_node",
    "critic_node"
)

workflow.add_edge(
    "critic_node",
    END
)


graph = workflow.compile()