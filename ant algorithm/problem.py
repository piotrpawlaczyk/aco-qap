from dataclasses import dataclass
from typing import Sequence

# Dane problemu
@dataclass
class QAPProblem:
    flow: Sequence[Sequence[int]]
    distance: Sequence[Sequence[int]]

    @property
    def size(self) -> int:
        return len(self.flow)

# Funkcja celu QAP
def qap_cost(problem: QAPProblem, assignment: Sequence[int]) -> int:
    """assignment[location] = factory"""
    n = problem.size
    cost = 0

    for i in range(n):
        for j in range(n):
            cost += problem.flow[ assignment[i] ][ assignment[j] ] * problem.distance[i][j]
    return cost