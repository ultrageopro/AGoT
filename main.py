"""AGoT with Heritage."""

import logging

from process.main_alg import agot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    query = "Какова комовинговая дистанция для объекта на красном смещении z=1?"
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

    logger.info("=== Результат AGoT с наследием (heritage) ===")
    logger.info("Итоговый ответ: %s", final_answer)
    logger.info("Всего узлов: %d", graph.nodes_count)

    for layer_id, layer in enumerate(graph.layers):
        logger.info("Layer %s\n%s\n", layer_id, layer)
