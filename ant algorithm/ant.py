from __future__ import annotations

from problem import *
from heuristic import *
from qap_types import *
import random


class Ant:
    def __init__(self, problem: QAPProblem):
        self.problem = problem
        self.assignment: list[int] = []
        self.cost: float = float("inf")

    def __str__(self):
        return str(self.assignment) + str(self.cost)
    
    @staticmethod
    def ant_solution(problem: QAPProblem, pheromones: list[list[float]],
        heuristic_strategy: HeuristicStrategyType, assigment_strategy: AssigmentStrategyType,) -> Ant:
        ant = Ant(problem)
        ant.build_solution(pheromones, heuristic_strategy, assigment_strategy)
        return ant
    
    def build_solution(self,
        pheromones: list[list[float]],
        heuristic_strategy: HeuristicStrategyType,
        assigment_strategy: AssigmentStrategyType,
    ) -> None:
        n = self.problem.size

        available_factories = list(range(n))
        asigment_factories = []
        assignment_map = {}   # assignment[location] = factory

        for location in random.sample(range(n), k=n):
            # heurystyka liczona dla aktualnej lokalizacji

            heuristic_values = heuristic_strategy(assignment_map, available_factories, location, self.problem)
            scores = assigment_strategy(
                [pheromones[location][factory] for factory in available_factories], heuristic_values )

            total = sum(scores)

            if total == 0:
                chosen_factory = random.choice(available_factories)
            else:
                probabilities = [score / total for score in scores]

                chosen_factory = random.choices(available_factories, weights=probabilities, k=1)[0]

            assignment_map[location] = chosen_factory
            available_factories.remove(chosen_factory)
            asigment_factories.append(chosen_factory)

        self.assignment = [-1] * n 
        
        for location, factory in assignment_map.items():
            self.assignment[location] = factory

        self.cost = qap_cost(self.problem, self.assignment)

