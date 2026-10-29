from __future__ import annotations

from typing import Callable, List, Sequence
from problem import QAPProblem


# Ocena dostępnych fabryk dla bieżącej lokalizacji.
def distance_heuristic(asigment_factories: dict[int, int], available_factories: Sequence[int], 
                        location: int, problem: QAPProblem) -> list[float]:
    """Preferuje przypisania o małym przyroście kosztu rozwiązania."""
    
    values = []
    for chosen_factory in available_factories:
        delta = 0
        for assigment_location, assigment_fabric in asigment_factories.items():
            delta += (
                problem.flow[chosen_factory][assigment_fabric] * problem.distance[location][assigment_location]
                + problem.flow[assigment_fabric][chosen_factory] * problem.distance[assigment_location][location]
            )
        
        values.append(1.0 / delta if delta  else 1)

    return values