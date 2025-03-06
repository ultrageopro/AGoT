"""Layer for AGoTGraph."""

from collections import UserList
from collections.abc import Iterator
from typing import override

from .node import Node


class Layer(UserList[Node | None]):
    """Слой графа AGoT."""

    def __init__(self, layer: list[Node | None], nmax: int) -> None:
        """Initialize an Layer instance.

        Args:
            layer (list[Node | None]): A list of nodes for this layer.
            nmax (int): The maximum number of nodes in this layer.

        """
        super().__init__(layer)
        self.nmax = nmax

    @override
    def __repr__(self) -> str:
        str_node_list: list[str] = []
        for node in self:
            layer, position = node.heritage[-1]
            node_str = str(
                f"[layer: {layer};\tposition: {position};\t"
                f"node_id: {node.node_id}];\nthought: {node.thought};",
            )
            str_node_list.append(node_str)
        return "\n".join(str_node_list)

    @override
    def __len__(self) -> int:
        return len([i for i in self.data if i])

    @override
    def __iter__(self) -> Iterator[Node]:
        return iter([i for i in self.data if i])

    @override
    def append(self, item: Node | None) -> None:
        msg = "Layer is full!"
        if len(self) > self.nmax:
            raise ValueError(msg)
        return super().append(item)
