# Strategie odkładania feromonów
from ant import Ant
from typing import Callable


# Wzmacnia feromony na podstawie kosztów rozwiązań i dodatkowo nagradza najlepszą mrówkę.
def global_reinforcement(reinforcement_strength: float, best_ant_bonus_strength:float, 
                        delta_fulction: Callable[[float], float] = lambda x:x):
    current_strength = reinforcement_strength
    current_best_ant_bonus_strength = best_ant_bonus_strength

    def reset() -> None:
        nonlocal current_strength, current_best_ant_bonus_strength
        current_strength = reinforcement_strength
        current_best_ant_bonus_strength = best_ant_bonus_strength

    def reinforcement(pheromones: list[list[float]], ant: Ant, strength: float):
        delta = delta_fulction(strength / ant.cost)

        # ant.assignment[location] = factory
        for location, factory in enumerate(ant.assignment):
            pheromones[location][factory] += delta

    def reinforcement_ants(pheromones: list[list[float]], ants: list[Ant]) -> None:
        nonlocal current_strength
        nonlocal current_best_ant_bonus_strength
        
        percent_dominaion = [ max(row) / sum(row) for row in pheromones]
        if(sum(percent_dominaion) / len(percent_dominaion) < 0.1 ):
            current_strength *= 1.01
            current_best_ant_bonus_strength *= 1.01
        elif(sum(percent_dominaion) / len(percent_dominaion) < 0.28 ):
            current_strength *= 1.001
            current_best_ant_bonus_strength *= 1.001
        else:
            current_strength *= 1.0002
            current_best_ant_bonus_strength *= 1.0002
        for ant in ants:
            reinforcement(pheromones, ant, current_strength)
        
        best_ant =  min(ants, key=lambda ant: ant.cost)

        
        reinforcement(pheromones, best_ant, current_best_ant_bonus_strength)

    reinforcement_ants.reset = reset
    return reinforcement_ants
