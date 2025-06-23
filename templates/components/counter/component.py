from pydantic import Field
from templates.base import BaseComponent


class Counter(BaseComponent):
    """A component representing the current count and its controls."""

    count: int = Field(..., description="The current count value.")
    title: str = Field(
        "HTMX Counter SPA", description="The title for the counter section."
    )
