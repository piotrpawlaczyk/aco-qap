# Ant Colony Optimization for QAP

A Python implementation of **Ant Colony Optimization (ACO)** for the **Quadratic Assignment Problem (QAP)**, developed as a university coursework project.

The project explores how pheromone influence, heuristic influence, colony size, and evaporation affect solution quality. It includes parameter experiments, visualizations, benchmark instances, and a project report.

The source comments, console output, chart labels, and report are primarily in Polish.

## Problem

QAP assigns facilities to locations while minimizing the total cost of flows between facilities multiplied by the distances between their assigned locations.

In this implementation, `assignment[location] = facility`. ACO constructs candidate assignments using pheromone trails and a heuristic based on the incremental assignment cost. Lower objective values indicate better solutions.

## Features

- Configurable influence of pheromones (`alpha`) and the heuristic (`beta`).
- Probabilistic assignment selection with an additional preference for the most attractive candidate.
- Pheromone reinforcement based on solution cost, with an additional reward for the best ant.
- Bounded pheromone levels and optional double evaporation for assignments not reinforced during an iteration.
- Elite solution retention between iterations.
- Repeated runs with mean cost trajectories and sample standard deviations.
- Parameter comparison plots and an assignment heatmap utility.

## Getting started

Use **Python 3.10 or newer**. Open a terminal in the directory containing `main.py`, then install the dependencies and run the program:

```sh
python -m pip install numpy matplotlib
python main.py
```

By default, `main.py` runs five trials on the `mine2` instance and prints the results to the terminal. This default command does not open a chart. To select another instance, change the final `instance("mine2")` call in `main.py`.

Instance names correspond to files in `qaplib/in/`, without the `.txt` extension. Preserve their capitalization when running on a case-sensitive filesystem.

## Running experiments

From the project directory, use the following commands to compare parameter configurations:

```sh
# Pheromone and heuristic influence
python -c "from main import run_alpha_beta; run_alpha_beta('mine3')"

# Colony size
python -c "from main import run_population; run_population('mine3')"

# Evaporation rate and single vs. double evaporation
python -c "from main import run_evaporate; run_evaporate('mine3')"
```

These experiments perform multiple runs and display Matplotlib charts. They can take considerably longer than the default example.

For a custom run and a plot of the mean best-so-far cost, use:

```python
from main import instance, make_chart

best, times, costs, costs_std, average_iterations = instance(
    "Chr12a",
    number_instance=5,
    ants_count=25,
    iterations_q=1.0,
)

print("Best cost:", best)
make_chart(times, costs)
```

`iterations_q` scales the iteration budget. Use at least two trials when requesting statistics through `instance()`.

## Data and report

Standard benchmark instances come from **QAPLIB**:

- [QAPLIB at Lehigh University](https://coral.ise.lehigh.edu/data-sets/qaplib/)
- Original download source: https://qaplib.mgi.polymtl.ca/

The custom instances `mine1`, `mine2`, and `mine3` were generated for this project. They cover relatively uniform flows, flows with larger outliers, and clustered flows, respectively.

`loader.py` includes their generators. Running `python loader.py` **overwrites** these three instance files with newly generated data.

- [Project report in Polish](raport.docx)
- [Saved experiment plots](wyniki/)

The report and saved plots document the coursework experiments. The current code includes subsequent fixes, including resetting evaporation and reinforcement state between runs, so new results may differ from the recorded results.

## Project structure

| File or directory | Purpose |
| --- | --- |
| `main.py` | ACO execution, repeated trials, statistics, and parameter experiments |
| `ant.py` | Construction of individual ant solutions |
| `problem.py` | QAP representation and objective function |
| `heuristic.py` | Incremental assignment cost heuristic |
| `assigment_strategy.py` | Assignment scoring strategies |
| `evaporation.py` | Pheromone evaporation |
| `reinforcement.py` | Pheromone reinforcement |
| `qap_types.py` | Shared strategy type definitions |
| `loader.py` | Instance loading and custom data generation |
| `heat_map.py` | Assignment heatmap utility |
| `qaplib/in/` | Benchmark and custom instances |
| `wyniki/` | Saved plots |
| `raport.docx` | Coursework report in Polish |

## Authorship

**Piotr Pawlaczyk** authored the ACO implementation, the report introduction, comparative experiments, analysis, and conclusions.

The report also compares ACO with a **Bees Algorithm (BA) implementation by Radosław Kmiotek**, developed as part of the shared university project. The BA implementation and its execution code are not included in this repository. The included code runs ACO independently; reproducing the ACO–BA comparison requires the separate BA implementation.

As disclosed in the report, AI assistance was used for debugging, plotting code, and selected implementation details, including the ACO heuristic.
