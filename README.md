# Ant Colony Optimization for QAP

A Python implementation of Ant Colony Optimization (ACO) for the Quadratic Assignment Problem (QAP), developed as a university project. Includes parameter experiments, plots, and a report in Polish.

## Run

Requires Python 3.10+ with NumPy and Matplotlib. Run from the directory containing `main.py`:

```sh
python -m pip install numpy matplotlib
python main.py
```

By default, the program runs five trials on `mine2` and prints the results. Change `instance("mine2")` at the end of `main.py` to select another instance from `qaplib/in/`.

Parameter experiments are available through `run_alpha_beta()`, `run_population()`, and `run_evaporate()` in `main.py`. For example:

```sh
python -c "from main import run_alpha_beta; run_alpha_beta('mine3')"
```

## Data and results

Benchmark instances come from [QAPLIB](https://coral.ise.lehigh.edu/data-sets/qaplib/), originally downloaded from https://qaplib.mgi.polymtl.ca/. The custom instances `mine1`, `mine2`, and `mine3` were generated for this project.

See the [report in Polish](raport.docx) and [experiment plots](wyniki/). They document earlier coursework experiments; subsequent code fixes may affect reproduced results.

## Authors

**Piotr Pawlaczyk** — ACO implementation, report introduction, comparative experiments, analysis, and conclusions.

The report compares ACO with a Bees Algorithm implementation by **Radosław Kmiotek**, developed within the shared university project. The BA code is not included.