"""Order model definition for SQLModel."""

from typing import Optional
from sqlmodel import SQLModel, Field


class Order(SQLModel, table=True):
    """
    Represents an order record in the database.

    Attributes:
        id (Optional[int]): Primary key, auto-incremented.
        item (str): Name of the item ordered.
        quantity (int): Quantity of the item.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    item: str
    quantity: int
