# fullstack-algo-lab
Modern Full-Stack Developer Laboratory Manual  A progressive, hands-on engineering path to build, test, containerize, and operate a production-like application laboratory locally on Windows 11 (WSL2 + PowerShell 7).

## Python algorithm assessment

Install the development tools and run the complete pytest pipeline:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/algorithms/test-all.py
```

Run one test file or filter by test name:

```bash
python scripts/algorithms/test-all.py --test-file "algorithms/arrays/Top K Frequent Elements/test_solution.py"
python scripts/algorithms/test-all.py --test-name "top_k"
```

Pytest discovers `test_*.py` and `*_test.py` files below `algorithms/`. The same suite runs automatically in GitHub Actions through `.github/workflows/test-python.yml`.
