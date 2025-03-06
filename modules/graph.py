"""Graph for AGoT."""

import uuid

from .base import Answer, Edge, Heritage
from .layer import Layer
from .node import Node


class AGoTGraph:
    """Класс для хранения текущего графа и финального ответа."""

    def __init__(self, graph_id: uuid.UUID, lmax: int, nmax: int) -> None:
        """Initialize an AGoTGraph instance.

        Args:
            graph_id (uuid.UUID): Unique identifier for this graph.
            lmax (int): The maximum number of layers in the graph.
            nmax (int): The maximum number of nodes in each layer.

        """
        self.graph_id = graph_id
        self.layers: list[Layer] = []
        self.edges: list[Edge] = []
        self.final_answer: Answer | None = None

        self.nmax = nmax
        self.lmax = lmax

    def add_node(self, node: Node) -> None:
        """Add a new node to the graph.

        Args:
            node (Node): The node to add, which must have a unique node_id.

        """
        layer, position = node.heritage[-1]

        while len(self.layers) <= layer:
            self.__new_layer()

        self.layers[layer][position] = node

    def add_edge(self, parent_id: str, child_id: str) -> None:
        """Add a new edge to the graph.

        Args:
            parent_id (str): The node_id of the parent node.
            child_id (str): The node_id of the child node.

        """
        self.edges.append((parent_id, child_id))

    def get_node(self, node: uuid.UUID | Heritage | tuple[int, int]) -> Node | None:
        """Get a node from the graph by its node_id.

        Args:
            node (uuid.UUID | Heritage): The node_id of the node to retrieve.

        Returns:
            Node: The node with the specified node_id.

        Raises:
            ValueError: If the node_id is not found in the graph.

        """
        match node:
            case uuid.UUID():
                return self.__get_node_by_id(node)
            case list():
                layer, position = node[-1]
                return self.layers[layer][position]
            case tuple():
                layer, position = node
                return self.layers[layer][position]
            case _:
                msg = f"Invalid node type: {type(node)}"
                raise ValueError(msg)

    def get_heritage_of_nodes(self, heritage: Heritage) -> list[Node]:
        """Get a list of nodes from the graph by their heritage.

        Args:
            heritage (Heritage): The heritage of the nodes to retrieve.

        Returns:
            list[Node]: A list of nodes with the specified heritage.

        Raises:
            ValueError: If any of the nodes in the heritage are not found in the graph.

        """
        msg = "Node with index {ind} not found"
        result: list[Node] = []
        for s_i in heritage:
            node = self.get_node(s_i)
            if node is None:
                raise ValueError(msg.format(ind=s_i))
            result.append(node)
        return result

    def __new_layer(self) -> None:
        """Add a new layer to the graph."""
        new_layer = Layer([None] * self.nmax, self.nmax)
        self.layers.append(new_layer)

    def __get_node_by_id(self, node_id: uuid.UUID) -> Node:
        """Get a node from the graph by its node_id.

        Args:
            node_id (uuid.UUID): The node_id of the node to retrieve.

        Returns:
            Node: The node with the specified node_id.

        Raises:
            ValueError: If the node_id is not found in the graph.

        """
        for layer in self.layers:
            for node in layer:
                if node is not None and node.node_id == node_id:
                    return node
        msg = f"Node with id {node_id} not found"
        raise ValueError(msg)

    @property
    def layers_count(self) -> int:
        """The number of layers in the graph.

        Returns:
            int: The number of layers in the graph.

        """
        return len(self.layers)

    @property
    def nodes_count(self) -> int:
        """The total number of nodes in the graph.

        Returns:
            int: The total number of nodes in the graph.

        """
        return sum(len(layer) for layer in self.layers)

    @property
    def edges_count(self) -> int:
        """The total number of edges in the graph.

        Returns:
            int: The total number of edges in the graph.

        """
        return len(self.edges)
