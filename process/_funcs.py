"""Functions for AGoT."""

from modules import AGoTGraph
from modules.base import Answer, Edge, Strategy, Thought


def t_empty(q: str, nmax: int) -> tuple[list[Thought], Strategy]:
    """Аналог T∅ из статьи: генерируем начальные мысли (верхний уровень).

    Args:
        q (str): исходный запрос
        nmax (int): максимальное кол-во мыслей

    Returns:
        tuple[list[Thought], Strategy]: список мыслей и стратегия

    """
    thoughts = [f"Initial thought about: {q}"][:nmax]
    return thoughts, "Strategy_for_initial_layer"


def t_0(
    q: str,
    parent_graph: AGoTGraph | None,
    nmax: int,
) -> tuple[list[Thought], Strategy]:
    """Аналог T0 из статьи: начальные мысли для вложенного графа.

    Args:
        q (str): исходный запрос
        parent_graph (AGoTGraph | None): родительский граф
        nmax (int): максимальное кол-во мыслей

    Returns:
        tuple[list[Thought], Strategy]: список мыслей и стратегия

    Raises:
        ValueError: если родительский граф None

    """
    msg = "Parent graph is None"
    if parent_graph is None:
        raise ValueError(msg)
    thoughts = [f"Nested initial thought about: {q}"][:nmax]
    return thoughts, "Strategy_for_nested_layer"


def t_general(
    q: str,
    current_graph: AGoTGraph,
    nmax: int,
) -> tuple[list[Thought], Strategy, list[Edge]]:
    """Аналог Te из статьи: генерируем мысли и рёбра.

    Args:
        q (str): исходный запрос
        current_graph (AGoTGraph): текущий граф
        nmax (int): максимальное кол-во мыслей

    Returns:
        tuple[list[Thought], Strategy, list[Edge]]: список мыслей, стратегия и рёбра

    """
    _ = current_graph
    thoughts = [f"Thought_{i}_for_{q}" for i in range(nmax)]
    strategy = f"Strategy_for_{q}"
    new_edges: list[Edge] = []
    return thoughts, strategy, new_edges


def is_complex(thought: Thought, current_graph: AGoTGraph) -> bool:
    """Аналог функции C: определяем, сложная ли мысль.

    Args:
        thought (Thought): мысль
        current_graph (AGoTGraph): текущий граф

    Returns:
        bool: True, если мысль сложная, False в противном случае

    """
    _ = current_graph
    return "complex" in thought.lower()


def evaluate_thought(thought: Thought, current_graph: AGoTGraph) -> Answer:
    """Аналог функции Eval: выдаём ответ для мысли.

    Args:
        thought (Thought): мысль
        current_graph (AGoTGraph): текущий граф

    Returns:
        Answer: ответ

    """
    _ = current_graph
    return f"Answer_for({thought})"


def final_thought_selector(current_graph: AGoTGraph) -> Thought:
    """Аналог функции Φ.

    Выбираем финальную мысль (например, последний некомплексный узел).

    Args:
        current_graph (AGoTGraph): текущий граф

    Returns:
        Thought: финальная мысль

    """
    candidates = [n for n in current_graph.layers[-1] if not n.is_complex]
    return candidates[-1].thought
