"""
mathforge/__main__.py

Command-line entry point for MathForge.

Usage
-----
One-shot:
    python -m mathforge "1/3 + 1/3 + 1/3"

Interactive:
    python -m mathforge
    (then type expressions, one per line; "exit" or "quit" to stop)
"""

import sys

from mathforge.parser.evaluator import evaluate_string
from mathforge.arithmetic.numbers.fraction import Fraction
from mathforge.core.errors import MathForgeError


def format_result(result: Fraction) -> str:
    """
    Format a Fraction for display: plain integer if whole, "numerator/denominator" otherwise.

    Parameters
    ----------
    result : Fraction

    Returns
    -------
    str
    """
    if result.denominator == 1:
        return str(result.numerator)
    return f"{result.numerator}/{result.denominator}"


def run_expression(source: str) -> int:
    """
    Evaluate one expression string and print the result or a clean error message.

    Parameters
    ----------
    source : str

    Returns
    -------
    int
        0 on success, 1 on error — a conventional shell exit code,
        used by main() when running in one-shot mode.
    """
    try:
        result = evaluate_string(source)
        print(format_result(result))
        return 0
    except MathForgeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def run_interactive() -> None:
    """
    Run an interactive read-evaluate-print loop until the user types "exit", "quit", or sends EOF (Ctrl-D).
    """
    print("MathForge interactive calculator. Type 'exit' to quit.")
    while True:
        try:
            line = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        stripped = line.strip()
        if stripped.lower() in ("exit", "quit"):
            break
        if not stripped:
            continue

        run_expression(stripped)


def main() -> int:
    """
    Entry point. Dispatches to one-shot or interactive mode based
    on whether a command-line argument was given.

    Returns
    -------
    int
        Exit code (0 success, 1 error) — only meaningful in
        one-shot mode; interactive mode always returns 0.
    """
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        return run_expression(expression)

    run_interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())