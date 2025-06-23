import random
from typing import List, Dict, Any, Tuple


def generate_simple_flow_data(
    title: str = "Simple Flow",
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate a simple 3-node flow diagram.

    Returns:
        Tuple of (title, nodes, edges)
    """
    nodes = [
        {
            "id": "1",
            "type": "input",
            "data": {"label": "Start"},
            "position": {"x": 250, "y": 25},
        },
        {"id": "2", "data": {"label": "Process"}, "position": {"x": 100, "y": 125}},
        {
            "id": "3",
            "type": "output",
            "data": {"label": "End"},
            "position": {"x": 250, "y": 250},
        },
    ]

    edges = [
        {"id": "e1-2", "source": "1", "target": "2"},
        {"id": "e2-3", "source": "2", "target": "3"},
    ]

    return title, nodes, edges


def generate_decision_flow_data(
    title: str = "Decision Flow",
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate a flow diagram with decision points.

    Returns:
        Tuple of (title, nodes, edges)
    """
    nodes = [
        {
            "id": "1",
            "type": "input",
            "data": {"label": "Start"},
            "position": {"x": 250, "y": 25},
        },
        {
            "id": "2",
            "type": "default",
            "data": {"label": "Decision"},
            "position": {"x": 250, "y": 125},
        },
        {
            "id": "3",
            "data": {"label": "Yes Path"},
            "position": {"x": 100, "y": 225},
        },
        {
            "id": "4",
            "data": {"label": "No Path"},
            "position": {"x": 400, "y": 225},
        },
        {
            "id": "5",
            "type": "output",
            "data": {"label": "End"},
            "position": {"x": 250, "y": 325},
        },
    ]

    edges = [
        {"id": "e1-2", "source": "1", "target": "2"},
        {"id": "e2-3", "source": "2", "target": "3", "label": "Yes"},
        {"id": "e2-4", "source": "2", "target": "4", "label": "No"},
        {"id": "e3-5", "source": "3", "target": "5"},
        {"id": "e4-5", "source": "4", "target": "5"},
    ]

    return title, nodes, edges


def generate_workflow_data(
    title: str = "Workflow Process",
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate a more complex workflow diagram.

    Returns:
        Tuple of (title, nodes, edges)
    """
    nodes = [
        {
            "id": "1",
            "type": "input",
            "data": {"label": "Submit Request"},
            "position": {"x": 250, "y": 25},
        },
        {
            "id": "2",
            "data": {"label": "Validate"},
            "position": {"x": 250, "y": 100},
        },
        {
            "id": "3",
            "type": "default",
            "data": {"label": "Valid?"},
            "position": {"x": 250, "y": 175},
        },
        {
            "id": "4",
            "data": {"label": "Reject"},
            "position": {"x": 100, "y": 250},
        },
        {
            "id": "5",
            "data": {"label": "Process"},
            "position": {"x": 400, "y": 250},
        },
        {
            "id": "6",
            "data": {"label": "Review"},
            "position": {"x": 400, "y": 325},
        },
        {
            "id": "7",
            "type": "output",
            "data": {"label": "Complete"},
            "position": {"x": 400, "y": 400},
        },
    ]

    edges = [
        {"id": "e1-2", "source": "1", "target": "2"},
        {"id": "e2-3", "source": "2", "target": "3"},
        {"id": "e3-4", "source": "3", "target": "4", "label": "No"},
        {"id": "e3-5", "source": "3", "target": "5", "label": "Yes"},
        {"id": "e5-6", "source": "5", "target": "6"},
        {"id": "e6-7", "source": "6", "target": "7"},
    ]

    return title, nodes, edges


def generate_random_flow_data(
    num_nodes: int = 5, title: str = "Random Flow"
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate a random flow diagram with specified number of nodes.

    Args:
        num_nodes: Number of nodes to generate
        title: Title for the flow diagram

    Returns:
        Tuple of (title, nodes, edges)
    """
    nodes = []
    edges = []

    # Node types for variety
    node_types = ["input", "default", "output"]
    node_labels = [
        "Start",
        "Process",
        "Validate",
        "Review",
        "Approve",
        "Reject",
        "Complete",
        "End",
    ]

    for i in range(num_nodes):
        node_id = str(i + 1)

        # Determine node type
        if i == 0:
            node_type = "input"
        elif i == num_nodes - 1:
            node_type = "output"
        else:
            node_type = random.choice(node_types)

        # Generate position
        x = random.randint(50, 450)
        y = 25 + (i * 75)

        # Generate label
        if i == 0:
            label = "Start"
        elif i == num_nodes - 1:
            label = "End"
        else:
            label = random.choice(node_labels)

        nodes.append(
            {
                "id": node_id,
                "type": node_type,
                "data": {"label": label},
                "position": {"x": x, "y": y},
            }
        )

        # Create edges (connect each node to the next)
        if i > 0:
            edges.append(
                {
                    "id": f"e{i}-{i + 1}",
                    "source": str(i),
                    "target": str(i + 1),
                }
            )

    return title, nodes, edges


def generate_flow_data_by_type(
    flow_type: str = "simple",
) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate flow data based on the specified type.

    Args:
        flow_type: Type of flow to generate ("simple", "decision", "workflow", "random")

    Returns:
        Tuple of (title, nodes, edges)
    """
    if flow_type == "simple":
        return generate_simple_flow_data()
    elif flow_type == "decision":
        return generate_decision_flow_data()
    elif flow_type == "workflow":
        return generate_workflow_data()
    elif flow_type == "random":
        return generate_random_flow_data()
    else:
        raise ValueError(f"Unknown flow type: {flow_type}")
