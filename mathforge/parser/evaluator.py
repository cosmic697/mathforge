"""
mathforge/parser/evaluator.py

Evaluator

Walks an AST (built by parser.py) and computes its numeric result.

This is the final stage of the pipeline:
    string -> tokenize -> tokens -> parse -> AST -> evaluate -> float

Evaluation is naturally recursive, mirroring how the tree itself is built: to evaluate a BinaryOp, first evaluate its left child, then its right child, then combine with the operator. Evaluating a Number is the base case — it's already a value, nothing to recurse into.
"""

from mathforge.parser.ast_nodes import Number, BinaryOp
from mathforge.arithmetic.numbers.fraction import Fraction
from mathforge.core.errors import UndefinedOperationError, InvalidOperandError


_OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}


def evaluate(node) -> Fraction:
    """
    Recursively evaluate an AST node to an exact Fraction result.

    Parameters
    ----------
    node : Number or BinaryOp

    Returns
    -------
    Fraction

    Raises
    ------
    InvalidOperandError
        If node is not a Number or BinaryOp, if a Number holds a non-whole value (e.g. 3.14 — not representable exactly as a Fraction from a float), or if the operator is unknown.
    UndefinedOperationError
        If a BinaryOp divides by a right-hand side that evaluates to zero.
    """
    if isinstance(node, Number):
        if not node.value.is_integer():
            raise InvalidOperandError(
                f"only whole-number literals are supported in Fraction mode, got {node.value}"
            )
        return Fraction(int(node.value))

    if isinstance(node, BinaryOp):
        left_value = evaluate(node.left)
        right_value = evaluate(node.right)

        if node.operator == "+":
            return left_value + right_value
        if node.operator == "-":
            return left_value - right_value
        if node.operator == "*":
            return left_value * right_value
        if node.operator == "/":
            if right_value == Fraction(0):
                raise UndefinedOperationError("division by zero")
            return left_value / right_value

        raise InvalidOperandError(f"unknown operator '{node.operator}'")

    raise InvalidOperandError(f"cannot evaluate node of type {type(node).__name__}")

def evaluate_string(source: str) -> float:
    """
    Convenience function: tokenize, parse, and evaluate a raw expression string in one call.

    Parameters
    ----------
    source : str
        e.g. "3 + 4 * 2"

    Returns
    -------
    float

    Raises
    ------
    ParserError
        If the string is malformed (propagated from tokenize/parse).
    UndefinedOperationError
        If evaluation hits a division by zero.
    """
    from mathforge.parser.parser import Parser
    tree = Parser.from_string(source).parse()
    return evaluate(tree)