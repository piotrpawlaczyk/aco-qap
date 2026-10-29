# Strategie wysychania feromonów
from qap_types import EvaporationStrategyType


# Podwójne parowanie przyspiesza wygaszanie feromonów niewzmocnionych w iteracji.
def double_forgetten_evaporation(evaporation_rate: float, min_tau: float,  max_tau: float = float("inf"),
                                 isSngle: bool = False) -> EvaporationStrategyType:
    last_pheremones = None

    def reset() -> None:
        nonlocal last_pheremones
        last_pheremones = None

    def evaporation(pheromones: list[list[float]]) -> None:
        nonlocal last_pheremones
        for i in range(len(pheromones)):
            for j in range(len(pheromones[i])):
                if(not isSngle and not last_pheremones is None and last_pheremones[i][j] == pheromones[i][j]):
                    pheromones[i][j] = (pheromones[i][j] - min_tau) * (1.0 - evaporation_rate) + min_tau
                pheromones[i][j] = (pheromones[i][j] - min_tau) * (1.0 - evaporation_rate) + min_tau
                pheromones[i][j] = max(min_tau, min(max_tau, pheromones[i][j]))


        last_pheremones = [fabrics.copy() for fabrics in pheromones]
    
    evaporation.reset = reset
    return evaporation

