from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, Protocol, TYPE_CHECKING
from problem import QAPProblem

if TYPE_CHECKING:
    from ant import Ant

# Typy strategii wykorzystywanych przez algorytm mrówkowy.


AssigmentStrategyType = Callable[
    [list[float], list[float]], list[float]
]

# Strategia parowania modyfikuje przekazaną macierz feromonów.
EvaporationStrategyType = Callable[
    [list[list[float]]], None
]

# Strategia wzmacniania aktualizuje feromony na podstawie rozwiązań mrówek.
class ReinforcementStrategyType(Protocol):
    def __call__(
        self,
        pheromones: list[list[float]],
        ants: list["Ant"],
    ) -> None:
        ...

# Heurystyka ocenia dostępne fabryki dla lokalizacji na podstawie częściowego przypisania i danych QAP.
HeuristicStrategyType = Callable[[ dict[int, int], Sequence[int], int,  QAPProblem ], list[float]]