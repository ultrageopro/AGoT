"""AGoT."""

import logging
import uuid
from dataclasses import dataclass
from typing import TypedDict, Unpack

type Thought = str
type Answer = str
type Strategy = str
type Edge = tuple[str, str]  # (идентификатор_родитель, идентификатор_потомок)


class AGoTParams(TypedDict):
    lmax: int
    nmax: int


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@dataclass
class Node:
    node_id: uuid.UUID
    thought: Thought
    strategy: Strategy
    answer: Answer
    is_complex: bool
    parent_graph_id: str | None


class AGoTGraph:
    def __init__(self, graph_id: str) -> None:
        """Создает новый граф.

        :param graph_id: уникальный идентификатор графа
        """
        self.graph_id = graph_id
        self.nodes: dict[uuid.UUID, Node] = {}
        self.edges: list[Edge] = []
        self.final_answer: Answer | None = None

    def add_node(self, node: Node) -> None:
        """Добавляет узел в граф.

        :param node: узел, который нужно добавить
        """
        self.nodes[node.node_id] = node

    def add_edge(self, parent_id: str, child_id: str) -> None:
        """Добавляет ребро в граф между узлами с идентификаторами parent_id и child_id.

        :param parent_id: идентификатор узла-родителя
        :param child_id: идентификатор узла-потомка
        """
        self.edges.append((parent_id, child_id))


def t_empty(q: str, nmax: int) -> tuple[list[Thought], Strategy]:
    """Аналог функции T∅ из статьи: генерируем мысли на самом верхнем уровне.

    Возвращает список мыслей и стратегию.

    Args:
        q (str): Запрос.
        nmax (int): Максимальное количество нод.

    Returns:
        tuple[list[Thought], Strategy]: Список мыслей и стратегия

    """
    thoughts = [f"Initial thought about: {q}"][:nmax]
    return thoughts, "Strategy_for_initial_layer"


def t_0(
    q: str,
    parent_graph: AGoTGraph | None,
    nmax: int,
) -> tuple[list[Thought], Strategy]:
    """Аналог функции T0 из статьи: генерируем начальные мысли для вложенного графа.

    Возвращает список мыслей и стратегию.

    Args:
        q (str): Запрос.
        parent_graph (AGoTGraph): Родительский граф.
        nmax (int): Максимальное количество нод.

    Returns:
        tuple[list[Thought], Strategy]: Список мыслей и стратегия

    Raises:
        ValueError: Parent graph is None

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
    """Аналог функции Te из статьи: генерируем мысли и ребра для текущего слоя.

    Возвращает список мыслей, стратегию и список ребер.

    Args:
        q (str): Запрос.
        current_graph (AGoTGraph): Текущий граф.
        nmax (int): Максимальное количество нод.

    Returns:
        tuple[list[Thought], Strategy, list[Edge]]:
        Список мыслей, стратегия и список ребер

    """
    # Заглушка.
    _ = current_graph

    thoughts = [f"Thought_{i}_for_{q}" for i in range(nmax)]
    strategy = f"Strategy_for_{q}"
    new_edges: list[Edge] = []
    return thoughts, strategy, new_edges


def is_complex(thought: Thought, current_graph: AGoTGraph) -> bool:
    """Аналог функции C из статьи: проверяет, является ли мысль "сложной".

    Args:
        thought (Thought): Мысль.
        current_graph (AGoTGraph): Текущий граф.

    Returns:
        bool: True, если мысль сложная, False в противном случае

    """
    # Заглушка.
    _ = current_graph
    return "complex" in thought.lower()


def evaluate_thought(thought: Thought, current_graph: AGoTGraph) -> Answer:
    """Аналог функции Eval: оценивает/отвечает на мысль.

    Args:
        thought (Thought): Мысль.
        current_graph (AGoTGraph): Текущий граф.

    Returns:
        Answer: Ответ

    """
    # Заглушка.
    _ = current_graph
    return f"Answer_for({thought})"


def final_thought_selector(current_graph: AGoTGraph) -> Thought:
    """Аналог функции Φ (Phi): выбирает финальную мысль из текущего графа.

    Args:
        current_graph (AGoTGraph): Текущий граф.

    Returns:
        Thought: Финальная мысль

    """
    # Допустим, финальный узел — последний добавленный не-комплексный.
    candidates = [n for n in current_graph.nodes.values() if not n.is_complex]
    if not candidates:
        candidates = list(current_graph.nodes.values())
    return candidates[-1].thought


def agot(
    q: str,
    depth: int,
    max_depth: int,
    parent_graph: AGoTGraph | None = None,
    **kwargs: Unpack[AGoTParams],
) -> tuple[Answer, AGoTGraph]:
    """Аналог Algorithm 1 из статьи.

    AGoT(q, h, Ghp), здесь h (heritage) упростим до "depth",
    а Ghp — это parent_graph.

    Args:
        q (str): Запрос.
        depth (int): Глубина.
        max_depth (int): Максимальная глубина.
        parent_graph (AGoTGraph, optional): Родительский граф.
        **kwargs (Unpack[AGoTParams]): Параметры алгоритма

    Returns:
        tuple[Answer, AGoTGraph]: Ответ и граф

    """
    lmax = kwargs.get("lmax", 3)
    nmax = kwargs.get("nmax", 3)

    graph_id = str(uuid.uuid4())
    current_graph = AGoTGraph(graph_id=graph_id)

    # Проходим по слоям: l = 0..lmax-1
    for layer in range(lmax):
        if layer == 0 and depth == 0:
            # Первый слой "верхнего" графа
            thoughts, strategy = t_empty(q, nmax)
        elif layer == 0:
            # Первый слой вложенного графа
            thoughts, strategy = t_0(q, parent_graph, nmax)
        else:
            # Остальные случаи
            thoughts, strategy, edges = t_general(q, current_graph, nmax)
            # Добавляем новые рёбра в граф
            for e in edges:
                current_graph.add_edge(*e)

        # Перебираем каждую сгенерированную мысль
        for t in thoughts:
            # Проверяем, не финальная ли эта мысль (условие в статье "th' is final")
            # В примере — если слово 'final' встретится в t, считаем её финальной
            if "final" in t.lower():
                ans = evaluate_thought(t, current_graph)
                current_graph.final_answer = ans
                return ans, current_graph

            # Иначе добавляем узел
            node_id = uuid.uuid4()
            complex_flag = is_complex(t, current_graph)
            node = Node(
                node_id=node_id,
                thought=t,
                strategy=strategy,
                answer="",
                is_complex=complex_flag,
                parent_graph_id=(parent_graph.graph_id if parent_graph else None),
            )
            current_graph.add_node(node)

            # Если мысль сложная и глубина < max_depth -> рекурсия
            if complex_flag and depth < max_depth:
                sub_answer, _ = agot(
                    q=t,  # Рекурсия передаёт текущую мысль как новый запрос
                    depth=depth + 1,
                    max_depth=max_depth,
                    lmax=lmax,
                    nmax=nmax,
                    parent_graph=current_graph,
                )
                # После возвращения из рекурсии заполним ответ узла
                node.answer = sub_answer
            else:
                # Простая мысль: сразу даём ответ
                ans = evaluate_thought(t, current_graph)
                node.answer = ans

    # Если дошли до конца слоёв: возвращаем "финальную мысль" этого графа
    final_th = final_thought_selector(current_graph)
    final_ans = evaluate_thought(final_th, current_graph)
    current_graph.final_answer = final_ans
    return final_ans, current_graph


if __name__ == "__main__":
    # Допустим, у нас есть исходный запрос:
    query = "Какова комовинговая дистанция для объекта на красном смещении z=1?"
    # Параметры AGoT
    MAX_DEPTH = 1
    L_MAX = 3
    N_MAX = 3

    final_answer, graph = agot(
        q=query,
        depth=0,
        max_depth=MAX_DEPTH,
        lmax=L_MAX,
        nmax=N_MAX,
    )

    logger.info("=== Результат AGoT ===")
    logger.info("Итоговый ответ: %s", final_answer)
    logger.info("Всего узлов в графе: %d", len(graph.nodes))
    logger.info("Структура узлов:")
    for node_id, node in graph.nodes.items():
        logger.info("- Node %s", node_id)
        logger.info("  Thought: %s", node.thought)
        logger.info("  Strategy: %s", node.strategy)
        logger.info("  Answer: %s", node.answer)
        logger.info("  Complex?: %s", node.is_complex)
