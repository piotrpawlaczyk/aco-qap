# Strategie wyboru na podstawie feromonów + heurystyki
from qap_types import AssigmentStrategyType

def standard_score(alpha: float, beta: float) -> AssigmentStrategyType:
    def score(pheromone_values: list[float], heuristic_values: list[float]) -> list[float]:

        return [
            (tau**alpha) * (eta**beta)
            for tau, eta in zip(pheromone_values, heuristic_values)
        ]

    return score


def greedy_score(alpha: float, beta: float) -> AssigmentStrategyType:
    def score(pheromone_values: list[float], heuristic_values: list[float]) -> list[float]:
        base = standard_score(alpha, beta)(pheromone_values,  heuristic_values)
        base[base.index( max(base) ) ] *= (len(pheromone_values)*0.1+1)
        return base

    return score
