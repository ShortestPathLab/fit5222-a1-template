![banner](./banner.png)

# Piglet — Assignment 1

Piglet is a library of search algorithms you can reuse in your own code. This branch is the starter scaffold for assignment 1: you implement your path-finding algorithms in `question1.py`, `question2.py` and `question3.py`.

> **New to terminals, Git or Python environments?** Follow [GETTING_STARTED.md](GETTING_STARTED.md)
> instead. It sets the assignment up from scratch and ends with trains moving on your screen. The
> rest of this README assumes you are comfortable with the tooling.

## Requirements

- [uv](https://docs.astral.sh/uv/) — the only thing you need to install yourself.

uv provisions the correct Python interpreter (3.14.6, pinned in `.python-version`) and every dependency for you. You do not need to install Python separately.

## Setup

Clone the repo, then run a question straight away:

```bash
uv run python question1.py
```

There is no separate install step. The first `uv run` creates a virtual environment in `.venv` and installs the dependencies, including [Flatland](https://github.com/ShortestPathLab/flatland), the railway simulator the assignment questions run against; this takes a few minutes. Later runs skip it and start immediately. Prefixing a command with `uv run` runs it inside that environment, so there is no `activate` step to remember.

## The assignment

Each question file contains a dummy implementation that always takes the first available transition. Replace it with your own algorithm.

```bash
uv run python question1.py    # single-agent path finding
uv run python question2.py    # multi-agent, conflict-free
uv run python question3.py    # multi-agent with malfunctions and replanning
```

Two switches at the top of each question file control what a run prints and shows. `debug = True` gives a step-by-step account of each episode, and `visualizer = True` opens the simulation so you can watch the trains.

For finer control of the visualiser, assign a `VisualiserOptions` instead of `True`:

```python
visualizer = VisualiserOptions(delay=0.1, headless=True, wait=False)
```

`delay` is the pause between timesteps in seconds, `headless=True` serves the run to your browser instead of opening a window, and `wait=False` starts immediately rather than holding the first frame until you are watching. The full set of fields is listed, commented out, at the top of each question file.

Turn the visualiser off for full runs. Rendering every episode is far slower than simulating one, and the scoring table is all you need.

## Piglet command line

```bash
uv run piglet --help
```

Run a scenario:

```bash
uv run piglet -p ./example/example_n_puzzle_scenario.scen -f graph -s uniform
```

### Generating search traces

Use search traces to analyse and debug algorithms in [Posthoc](https://posthoc.pathfinding.ai). Add the `--log trace` argument to make Piglet output search traces.

```bash
uv run piglet -p ./example/arena2.min.scen -f graph -s a-star --log trace
```

## Piglet library

To run a search you need three things: a domain, an expander, and a search.

```python
from lib_piglet.domains import gridmap
from lib_piglet.expanders.grid_expander import grid_expander
from lib_piglet.search.graph_search import graph_search
from lib_piglet.search.search_node import compare_node_f
from lib_piglet.utils.data_structure import bin_heap
from lib_piglet.heuristics import gridmap_h

# a gridmap domain, and an expander that generates its successors
gm = gridmap.gridmap("./example/gridmap/empty-16-16.map")
expander = grid_expander(gm)

# a search, given an open list (a binary heap ordered on f) and the expander
search = graph_search(
    bin_heap(compare_node_f),
    expander,
    heuristic_function=gridmap_h.piglet_heuristic,
)

# for a gridmap, a state is an (x, y) tuple
solution = search.get_path((1, 2), (10, 2))
print(solution)
```

Every heuristic takes `(domain, current_state, goal_state)`, so any of them can be handed straight to a search. `piglet_heuristic` is the default each domain uses from the command line; swap in `gridmap_h.octile_heuristic`, `gridmap_h.straight_heuristic` or your own to compare. Use `compare_node_g` instead of `compare_node_f` for an uninformed search.
