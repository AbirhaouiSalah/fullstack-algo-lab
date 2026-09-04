# Executing Algorithm Tests

This guide explains how to run the algorithm test pipelines locally. 

## Python tests with pytest

From the repository root: fullstack-algo-lab, create a Python virtual environment, install the development dependencies, and run all tests:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python algorithms/test-all.py
```

The runner discovers Python tests below `algorithms/` matching:

- `test_*.py`
- `*_test.py`

### Run a specific test file

```bash
python algorithms/test-all.py \
  --test-file "algorithms/arrays/Top K Frequent Elements/test_solution.py"
```

### Filter tests by name

```bash
python algorithms/test-all.py --test-name "top_k"
```

You can also run pytest directly:

```bash
python -m pytest algorithms
python -m pytest algorithms -k "top_k"
```

## TypeScript tests with Vitest

Install the Node.js dependencies and run all TypeScript tests:

```bash
npm install
npm test
```

Run a specific TypeScript test file:

```bash
npx vitest run "algorithms/arrays/two-sum/solution.test.ts"
```

## macOS and Homebrew

Homebrew normally provides `python3`, not `python`. If `python` is not found,
use `python3` to create the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Use `python -m pip` after activation so pip installs packages into the same
Python environment that runs pytest.

## Continuous integration

Python tests run automatically in GitHub Actions through:

```text
.github/workflows/test-python.yml
```

The workflow installs `requirements-dev.txt` and executes the complete pytest
suite.
