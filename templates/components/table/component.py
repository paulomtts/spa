from enum import Enum
from typing import Any, Union
from pydantic import BaseModel, Field, field_validator
from templates.base import BaseComponent


class ColumnAlign(str, Enum):
    """Text alignment options for table columns."""

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class TableColumn(BaseModel):
    """Simple column definition."""

    label: str = Field(..., description="Display label for the column header")
    key: str = Field(..., description="Data key to access the value from row data")
    align: ColumnAlign = Field(
        default=ColumnAlign.LEFT, description="Text alignment for the column"
    )


class TableRow(BaseModel):
    """A structured representation of a single table row."""

    id: str | int
    data: dict[str, Any]
    class_name: str = Field(default="", description="Class name to apply to the row")


class TableComponent(BaseComponent):
    title: str = Field(..., description="Table title")
    columns: list[TableColumn] = Field(..., description="Table columns")
    rows: list[Union[TableRow, dict[str, Any]]] = Field(..., description="Table rows")

    @field_validator("rows", mode="before")
    def transform_rows(cls, v):
        """Transform raw row data into TableRow objects."""
        if not isinstance(v, list):
            return v

        transformed_rows = []
        for i, row in enumerate(v):
            if isinstance(row, dict):
                transformed_rows.append(
                    TableRow(
                        id=row.get("id", i),
                        data=row,
                        class_name=row.get("class_name", ""),
                    )
                )
            else:
                transformed_rows.append(row)

        return transformed_rows
