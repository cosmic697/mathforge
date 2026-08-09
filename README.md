# MathForge

> A modular mathematical computing platform, built from scratch in Python.

![Tests](https://github.com/cosmic697/mathforge/actions/workflows/tests.yml/badge.svg)

MathForge implements its core mathematical algorithms from scratch
rather than relying on NumPy/SciPy/SymPy — the goal is depth of
understanding and a from-scratch architecture, not competing with
those libraries on performance. See [docs/](docs/) for design notes.

## Quick start

```bash
pip install -e .
python3 -m mathforge "1/3 + 1/3 + 1/3"
# -> 1

python3 -m mathforge
>> 3 + 4 * 2
11
>> exit
```

## What's implemented

- **Arithmetic** — `Fraction`, `ComplexNumber`, `Decimal`, `Percentage`, all exact/immutable, with a shared error hierarchy
- **Linear Algebra** — `Vector` (dot/cross product, magnitude), `Matrix` (multiplication, transpose, determinant, inverse via Gaussian elimination with partial pivoting)
- **Parser** — hand-written tokenizer, recursive-descent parser, evaluator; wired to `Fraction` for exact results
- **Statistics** — `Dataset` with mean/median/mode/variance/std_dev, covariance, correlation, linear regression
- **Numerical Methods** — bisection, Newton-Raphson, and secant root-finding
- **CLI** — one-shot and interactive expression evaluation

Each module has its own `README.md`/`ROADMAP.md` under `mathforge/<module>/` tracking scope and progress.

## Status

Early, active development. See individual module ROADMAPs for what's next.