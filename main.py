# QAP – Ant Colony Optimization (ACO) w Pythonie
from __future__ import annotations

import random
random.seed(42)

from dataclasses import dataclass
from typing import Callable, List, Sequence

from problem import *
from qap_types import *
from heuristic import *
from assigment_strategy import *
from evaporation import *
from reinforcement import *
from ant import Ant
from loader import *

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import time
from bisect import bisect_right



def print_pheremons(pheromones: list[list[float]]):
    for location, fabrcis_pheromones in enumerate(pheromones):
        print(f"lokacja: {location}", end = " ")
        for fabrcis_pheromone in fabrcis_pheromones:
            print(round(fabrcis_pheromone, 2), end = " ")
        print()

    print("dominacja")
    percent_dominaion = ( 100  * max(row) / sum(row) for row in pheromones)
    bests = ( 1+ row.index(max(row)) for row in pheromones)
    for (i, val), best in zip( enumerate(percent_dominaion), bests):
       print(f"{i}: best pheromon {best}, {val}%")


def run_ant_colony(problem: QAPProblem, ants_count: int,
        iterations: int, 
        elite_size: int,
        heuristic_strategy: HeuristicStrategyType,
        assigment_strategy: AssigmentStrategyType,
        evaporation_strategy: EvaporationStrategyType,
        reinforcement_strategy: ReinforcementStrategyType,
        isDebug: bool = False,
        print_term_or_None: int | None = None,
        time_to_end = 0
        ):
    
    if(print_term_or_None is None):
        printTerm = iterations // 10
    else:
        printTerm = int(print_term_or_None)

    reset_evaporation = getattr(evaporation_strategy, "reset", None)
    if reset_evaporation is not None:
        reset_evaporation()

    reset_reinforcement = getattr(reinforcement_strategy, "reset", None)
    if reset_reinforcement is not None:
        reset_reinforcement()

    pheromones = [[1.0 for _ in range(problem.size)] for _ in range(problem.size)]

    best_solution = None
    best_cost = float("inf")
    startTime = time.perf_counter_ns() / 10**9

    ants = []
    prev_ants = []

    costs = []
    times = []
    iteration = 0
    while(True):
        iteration+=1
        if(time_to_end != 0 and time.perf_counter_ns() / 10**9 - startTime > time_to_end ):
            break
        if(time_to_end == 0 and iteration > iterations):
            break
        if(isDebug):
            print(f"iteracja: {iteration}")
        prev_ants = ants
        ants = []
        if(iteration > 1):
            for i in range(elite_size):
                ants.append(prev_ants[i])

        for i in range(elite_size, ants_count):
            ants.append(Ant.ant_solution(problem, pheromones, heuristic_strategy, assigment_strategy))
        
        reinforcement_strategy( pheromones, ants)

        ants = sorted(ants, key = lambda ant: ant.cost)
        ant = ants[0]
        if ant.cost < best_cost:
            best_cost = ant.cost
            best_solution = ant.assignment.copy()

        evaporation_strategy(pheromones)

        if isDebug and iteration % printTerm == 0:
            print("mrowki: ")
            for ant in ants:
                print(ant)
            print("ferominy: ")
            print_pheremons(pheromones)
            print(f"Koniec iteracji {iteration}, najlepszy koszt = {best_cost}")
        elif iteration % (iterations // 10) == 0:
            print(f"Koniec iteracji {iteration}, najlepszy koszt = {best_cost}")



        costs.append(best_cost)

        times.append(time.perf_counter_ns() / 10**9 - startTime)    


    return best_solution, best_cost, costs, times, iteration 


def make_chart(t: List[int], cost: List[float]):
    init_chart()
    add_to_chart(t, cost)
    display_chart()
    
def init_chart():
    plt.xlabel("Czas[s]")
    plt.ylabel("Koszt")

def add_to_chart(t: List[int], cost: List[float], name: str = ""):
    plt.plot(np.array(t), np.array(cost), label=f"{name}, wynik: {cost[-1]:.2f}")

def add_to_chart_with_std(t: List[int], cost_mean: List[float], cost_std: List[float],
                          best: float, name: str = ""):
    plt.plot(np.array(t), np.array(cost_mean), label=f"{name}, wynik sredni: {cost_mean[-1]:.2f}, wynik najlepszy: {best:.2f}")
    plt.fill_between(t, np.array(cost_mean) - np.array(cost_std), 
                    np.array(cost_mean) + np.array(cost_std), alpha=0.2)
        

def display_chart():
    plt.legend(loc="upper right")
    plt.show()

def instance(file_name, number_instance = 5,
    iterations_q = 1.0,
    ants_count = 25,
    elite_size = 1,
    heuristic_strategy = distance_heuristic,
    assigment_strategy = greedy_score(alpha=1.0, beta=1.0),
    evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.05, min_tau = 0.04, max_tau = 25),
    reinforcement_strategy = None,
    isDebug=False,
    time_to_end = 0) -> tuple[float, list[int], list[float], list[float], float]:

    problem = load_problem_from_file(file_name)

    if reinforcement_strategy is None:
        reinforcement_strategy = global_reinforcement(
            reinforcement_strength=1000,
            best_ant_bonus_strength=2,
            delta_fulction=lambda x: x*x
        )

    iterations = int(1_000 / math.sqrt(problem.size) * iterations_q)
    all_costs = []
    all_times = []
    best = float("inf")
    loops = []
    for i in range(number_instance):
        best_assignment, best_cost, costs , times, number_lop = run_ant_colony(
            problem=problem,
            iterations=iterations,
            ants_count=ants_count,
            elite_size=elite_size,
            heuristic_strategy=heuristic_strategy,
            assigment_strategy=assigment_strategy,
            evaporation_strategy=evaporation_strategy,
            reinforcement_strategy=reinforcement_strategy,
            isDebug=isDebug,
            time_to_end=time_to_end
            )
        best = min(best_cost, best)
        loops.append(number_lop)

        print("\nNajlepsze przypisanie:", best_assignment)
        print("Najlepszy koszt:", best_cost)
        if(not best_assignment is None):
            official_result = [0]*problem.size
            for location, fabric in enumerate(best_assignment):
                official_result[fabric] = location+1
            print("rowiazanie:", official_result)
        all_costs.append(costs)

        all_times.append(times)

    times, costs, costs_std = normalize_runs(all_times, all_costs)
    if(best_assignment is None):
        best_assignment = []
    return (best, times, costs, costs_std, sum(loops) / len(loops))


 
def normalize_runs(
    all_times: list[list[int]],
    all_costs: list[list[float]]
):
    size = len(all_costs)
    global_times = sorted({ t for times in all_times for t in times })

    normalized_costs = []
    for times, costs in zip(all_times, all_costs):
        run_costs = []

        for t in global_times:

            idx = bisect_right(times, t) - 1
            if idx < 0:
                run_costs.append(costs[0])
            else:
                run_costs.append(costs[idx])

        normalized_costs.append(run_costs)

    means_costs = []
    std_costs = []
    for i in range (len(global_times)):
        means_costs.append(  sum( 
             normalized_costs[run_costs][i] for run_costs in range( size )
                ) / size
        )
        variance = sum(
            (normalized_costs[run_costs][i] - means_costs[-1]) ** 2
            for run_costs in range(size)
            ) / (size - 1)

        std_costs.append(math.sqrt(variance))

    return global_times, means_costs, std_costs

  
def run(file_name):
    init_chart()
    names = [
        "alpha=1, beta=1, rozmiar=25, double, rate=0.4 ",
        "alpha=0.8, beta=1.25, rozmiar=25, double, rate=0.4 ",
        "alpha=1.25, beta=0.8, rozmiar=25, double, rate=0.4 ",
        "alpha=1, beta=1, rozmiar=40, double, rate=0.4 ",
        "alpha=1, beta=1, rozmiar=25, single, rate=0.4",
        ]
    
    q = 0.2 * 100
    number_run = 5
    startTime = time.perf_counter_ns() / 10**9

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       ants_count=25,
                                       assigment_strategy=greedy_score(alpha=1, beta=1),
                                       evaporation_strategy=double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[0])
    print(1/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       ants_count=25,
                                       assigment_strategy=greedy_score(alpha=0.8, beta=1.25),
                                       evaporation_strategy=double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[1])
    print(2/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       ants_count=25,
                                       assigment_strategy=greedy_score(alpha=1.25, beta=0.8),
                                       evaporation_strategy=double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[2])
    print(3/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q/40*25,
                                       ants_count=40,
                                       assigment_strategy=greedy_score(alpha=1, beta=1),
                                       evaporation_strategy=double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[3])
    print(4/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       ants_count=25,
                                       assigment_strategy=greedy_score(alpha=1, beta=1),
                                       evaporation_strategy=double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25, isSngle=True),
                                       )
    add_to_chart(times, costs, names[4])
    print(5/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    display_chart()

def run_evaporate(file_name):
    init_chart()
    names = [
        "podwojne, evaporation_rate = 0.05",
        "podwojne, evaporation_rate = 0.2",
        "podwojne, evaporation_rate = 0.4",
        "podwojne, evaporation_rate = 0.6",

        "pojedyncze, evaporation_rate = 0.2",
        "pojedyncze, evaporation_rate = 0.4",
        "pojedyncze, evaporation_rate = 0.6",

        ]
    
    q = 0.2 * 100
    number_run = 5
    startTime = time.perf_counter_ns() / 10**9

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.05, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[0])
    print(1/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.2, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[1])
    print(2/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[2])
    print(3/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.6, min_tau = 0.04, max_tau = 25),
                                       )
    add_to_chart(times, costs, names[3])
    print(4/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.2, min_tau = 0.04, max_tau = 25, isSngle=True),
                                       )
    add_to_chart(times, costs, names[4])
    print(5/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.4, min_tau = 0.04, max_tau = 25, isSngle=True),
                                       )
    add_to_chart(times, costs, names[5])
    print(6/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")
    
    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                       evaporation_strategy = double_forgetten_evaporation(evaporation_rate=0.6, min_tau = 0.04, max_tau = 25, isSngle=True),
                                       )
    add_to_chart(times, costs, names[6])
    print(7/7, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    display_chart()
   

def run_population(file_name):
    init_chart()
    names = [
        "rozmiar populacji = 5",
        "rozmiar populacji = 10",
        "rozmiar populacji = 25",
        "rozmiar populacji = 50",
        "rozmiar populacji = 100",
        ]
    
    q = 0.2 * 50
    number_run = 5
   
    startTime = time.perf_counter_ns() / 10**9

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q/5*50,
                                   ants_count=5)
    add_to_chart(times, costs, names[0])
    print(1/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q/10*50,
                                   ants_count=10)
    add_to_chart(times, costs, names[1])
    print(2/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q/25*50,
                                   ants_count=25)
    add_to_chart(times, costs, names[2])
    print(3/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                   ants_count=50)
    add_to_chart(times, costs, names[3])
    print(4/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q/100*50,
                                   ants_count = 100)
    add_to_chart(times, costs, names[4])
    print(5/5, time.perf_counter_ns() / 10**9 - startTime, "\n\n\n")

    
    display_chart()


def run_alpha_beta(file_name):
    init_chart()
    names = [
        "alpha = 0.4, beta = 2.5",
        "alpha = 0.8, beta = 1.28",
        "alpha = 1, beta = 1",
        "alpha = 1.25, beta = 0.8",
        "alpha = 2.5, beta = 0.4",
        ]
    
    q = 0.2 * 50
    number_run = 5

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                   assigment_strategy = greedy_score(alpha=0.4, beta=2.5))
    add_to_chart(times, costs, names[0])
    print(1/5, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                   assigment_strategy = greedy_score(alpha=0.8, beta=1.28))
    add_to_chart(times, costs, names[1])
    print(2/5, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                   assigment_strategy = greedy_score(alpha=1.0, beta=1.0))
    add_to_chart(times, costs, names[2])
    print(3/5, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                   assigment_strategy = greedy_score(alpha=1.25, beta=0.8))
    add_to_chart(times, costs, names[3])
    print(4/5, "\n\n\n")

    _, times, costs, costs_std, _ = instance(file_name, number_instance = number_run,  iterations_q=q,
                                   assigment_strategy = greedy_score(alpha=2.5, beta=0.4))
    add_to_chart(times, costs, names[4])
    print(5/5, "\n\n\n")

    
    display_chart()
    
if __name__ == "__main__":
    instance("mine2")
