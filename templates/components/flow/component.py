from pydantic import Field
from templates.base import BaseComponent


class FlowComponent(BaseComponent):
    """A component representing a ReactFlow diagram."""

    title: str = Field("Flow Diagram", description="The title for the flow section.")
    nodes: list = Field(default_factory=list, description="Flow nodes data.")
    edges: list = Field(default_factory=list, description="Flow edges data.")
