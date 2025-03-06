"""Main algorithm for AGoT."""

import uuid
from typing import Unpack

from modules import AGoTGraph, Node
from modules.base import AGoTParams, Answer, Edge, Heritage, Strategy, Thought

from ._process_functions import (
    evaluate_thought,
    final_thought_selector,
    is_complex,
    t_0,
    t_empty,
    t_general,
)


def _get_thoughts(
    layer_num: int,
    depth: int,
    query: str,
    parent_graph: AGoTGraph | None,
    nmax: int,
    current_graph: AGoTGraph,
) -> tuple[list[Thought], Strategy, list[Edge]]:
    """Генерирует мысли и стратегию в зависимости от текущего слоя и глубины.

    В зависимости от номера слоя и глубины эта функция выбирает соответствующий
    процесс генерации мыслей для графа AGoT. Она определяет начальные мысли
    и стратегию для верхнего уровня, вложенных слоев графа или общих случаев.

    Args:
        layer_num (int): Текущий номер слоя в графе.
        depth (int): Текущая глубина графа.
        query (str): Исходный запрос или задача для обработки.
        parent_graph (AGoTGraph | None): Родительский граф, если есть.
        nmax (int): Максимальное количество генерируемых мыслей.
        current_graph (AGoTGraph): Граф, который в данный момент обрабатывается.

    Returns:
        tuple[list[Thought], Strategy, list[Edge]]: Кортеж, содержащий
        список сгенерированных мыслей, используемую стратегию и
        список рёбер, созданных в процессе.

    """
    edges: list[Edge] = []
    if layer_num == 0 and depth == 0:
        # Верхний уровень, первый слой
        thoughts, strategy = t_empty(query, nmax)
    elif layer_num == 0:
        # Первый слой вложенного графа
        thoughts, strategy = t_0(query, parent_graph, nmax)
    else:
        # Остальные случаи
        thoughts, strategy, edges = t_general(query, current_graph, nmax)

    return thoughts, strategy, edges


# -------------------------
# Главная функция AGoT
# -------------------------
def agot(
    query: str,
    depth: int,
    parent_graph: AGoTGraph | None = None,
    current_heritage: list[tuple[int, int]] | None = None,
    **kwargs: Unpack[AGoTParams],
) -> tuple[Answer, AGoTGraph]:
    """Return the final answer and the final graph using AGoT algorithm.

    AGoT(q, h, Ghp) из статьи, где:
      - query: исходный запрос
      - depth: текущая глубина вложенности
      - max_depth: максимальная глубина
      - parent_graph: граф-родитель (может быть None, если верхний уровень)
      - current_heritage: текущее «наследие», список пар (layer_index, node_index)
      - lmax, nmax: параметры для кол-ва слоёв и кол-ва узлов в слое

    Returns:
        tuple[Answer, AGoTGraph]: финальный ответ и граф

    """
    # Инициализируем heritage, если не задан
    if current_heritage is None:
        current_heritage = []

    lmax = kwargs.get("lmax", 3)
    nmax = kwargs.get("nmax", 3)
    max_depth = kwargs.get("max_depth", 3)
    current_graph = AGoTGraph(graph_id=uuid.uuid4(), nmax=nmax, lmax=lmax)

    # Проходим по слоям: layer = 0..(lmax-1)
    for layer in range(lmax):
        # Генерация мыслей и стратегии
        thoughts, strategy, edges = _get_thoughts(
            layer_num=layer,
            depth=depth,
            query=query,
            parent_graph=parent_graph,
            nmax=nmax,
            current_graph=current_graph,
        )
        for e in edges:
            current_graph.add_edge(*e)

        # Перебираем мысли текущего слоя
        for i, t in enumerate(thoughts):
            # Проверка на «финальную» мысль
            if "final" in t.lower():
                ans = evaluate_thought(t, current_graph)
                current_graph.final_answer = ans
                return ans, current_graph

            # Создаём heritage для этого узла: добавляем (layer, i) к текущему наследию
            node_heritage: Heritage = [*current_heritage, (layer, i)]

            # Проверяем, сложная ли мысль
            complex_flag = is_complex(t, current_graph)

            # Создаём новый узел
            node = Node(
                node_id=uuid.uuid4(),
                thought=t,
                strategy=strategy,
                answer="",
                is_complex=complex_flag,
                parent_graph_id=(parent_graph.graph_id if parent_graph else None),
                heritage=node_heritage,
            )
            current_graph.add_node(node)

            # Если сложная мысль и глубина не достигла max_depth, уходим в рекурсию
            if complex_flag and depth < max_depth:
                sub_answer, _ = agot(
                    query=t,
                    depth=depth + 1,
                    max_depth=max_depth,
                    parent_graph=current_graph,
                    current_heritage=node_heritage,
                    lmax=lmax,
                    nmax=nmax,
                )
                # Запишем ответ узла после возвращения из рекурсии
                node.answer = sub_answer
            else:
                # Иначе сразу оцениваем мысль
                ans = evaluate_thought(t, current_graph)
                node.answer = ans

    # Если слои кончились, выбираем финальную мысль из графа
    final_th = final_thought_selector(current_graph)
    final_ans = evaluate_thought(final_th, current_graph)
    current_graph.final_answer = final_ans
    return final_ans, current_graph
