# graph.py

from warnings import warn
from typing import Any

class _EdgeData():
    def __init__(
        self,
        a: int,
        b: int,
        weight: float,
        a_to_b_meta: dict[str, Any] | None = None,
        b_to_a_meta: dict[str, Any] | None = None, 
    ) -> None:
        self.a: int = a
        self.b: int = b
        self.weight: float = weight
        self.a_to_b_meta: dict[str, Any] = a_to_b_meta or {}
        self.b_to_a_meta: dict[str, Any] = b_to_a_meta or {}

    def __repr__(self) -> str:
        return f"_EdgeData(a={self.a}, b={self.b}, weight={self.weight})"

    __str__ = __repr__

    def metadata_of(self, id: int) -> dict[str, Any]:
        if id == self.a:
            return self.a_to_b_meta
        elif id == self.b:
            return self.b_to_a_meta
        else:
            raise ValueError(f"Unrelated id {id} to this edge ({self.a}, {self.b})")


class _Node:
    def __init__(self, id: int) -> None:
        self.id: int = id 
        self.edges: dict[int, _EdgeData] = {}

    def __repr__(self) -> str:
        return f"_Node(id={self.id}, edges={list(self.edges.keys())})"

    __str__ = __repr__

    def connect(self, other_id: int, data: _EdgeData) -> None:
        self.edges[other_id] = data

    def disconnect(self, other_id: int) -> None:
        self.edges.pop(other_id, None)

    def is_connected(self, other_id: int) -> bool:
        return other_id in self.edges

    def get_edge_data(self, other_id: int) -> _EdgeData:
        return self.edges[other_id]
    

class Graph:
    def __init__(self) -> None:
        self._nodes: dict[int, _Node] = {}
        self._last_id: int = -1

    # --------------------- PRIVATE METHODS -------------------------

    def _get_node_by_id(self, id: int) -> _Node:
        if id not in self._nodes:
            raise RuntimeError(f"Cannot find node id {id} in graph.")
        return self._nodes[id]

    def _get_nodes_by_ids(self, *ids: int) -> list[_Node]:
        return [self._get_node_by_id(id) for id in ids]

    def _check_connected(self, a: _Node, b: _Node) -> bool:
        return a.is_connected(b.id) and b.is_connected(a.id)
    
    def _validate_weight(self, weight: float) -> None:
        if weight < 0:
            raise ValueError("Edge weight must be non-negative.")

    def _get_edge_data(self, a: int, b: int) -> _EdgeData:
        node_a, node_b = self._get_nodes_by_ids(a, b)
        if not self._check_connected(node_a, node_b):
            raise RuntimeError("Nodes are not connected.")
        return node_a.get_edge_data(b)

    # ----------------------- PUBLIC METHODS -------------------------

    def create_node(self) -> int:
        self._last_id += 1
        self._nodes[self._last_id] = _Node(self._last_id)
        return self._last_id

    def check_connected(self, a: int, b: int) -> bool:
        node_a, node_b = self._get_nodes_by_ids(a, b)
        return self._check_connected(node_a, node_b)

    def connect(
        self,
        a: int,
        b: int,
        weight: float = 1.0,
        a_to_b_meta: dict[str, Any] | None = None,
        b_to_a_meta: dict[str, Any] | None = None,
        overwrite: bool = True
    ) -> bool:
        data = _EdgeData(
            a=a,
            b=b,
            weight=weight,
            a_to_b_meta=a_to_b_meta,
            b_to_a_meta=b_to_a_meta
        )

        if data.a == data.b:
            warn("Cannot connect node to itself.")
            return False

        self._validate_weight(data.weight)

        node_a, node_b = self._get_nodes_by_ids(data.a, data.b)

        if not overwrite and self._check_connected(node_a, node_b):
            warn(f"Nodes {data.a} and {data.b} already connected. Use overwrite = True to update the edge weight.")
            return False

        node_a.connect(node_b.id, data)
        node_b.connect(node_a.id, data)
        return True

    def disconnect(self, a: int, b: int) -> None:
        node_a, node_b = self._get_nodes_by_ids(a, b)

        if not self._check_connected(node_a, node_b):
            warn("Nodes are not connected.")
            return
        
        node_a.disconnect(node_b.id)
        node_b.disconnect(node_a.id)

    def neighbors(self, id: int) -> set[int]:
        return set(self._get_node_by_id(id).edges.keys())

    def metadata_from_to(self, from_id: int, to_id: int) -> dict[str, Any]:
        return self._get_edge_data(from_id, to_id).metadata_of(from_id)

    def weight(self, a: int, b: int) -> float:
        return self._get_edge_data(a, b).weight