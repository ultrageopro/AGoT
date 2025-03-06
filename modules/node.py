"""Node for AGoTGraph."""

import uuid
from dataclasses import dataclass

from .base import Answer, Heritage, Strategy, Thought


@dataclass
class Node:
    """Узел графа AGoT."""

    node_id: uuid.UUID
    thought: Thought
    strategy: Strategy
    answer: Answer
    heritage: Heritage
    is_complex: bool
    parent_graph_id: uuid.UUID | None
