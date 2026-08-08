"""
mathforge/parser/evaluator.py

Evaluator

Walks an AST (built by parser.py) and computes its numeric result.

This is the final stage of the pipeline:
    string -> tokenize -> tokens -> parse -> AST -> evaluate -> float

Evaluation is naturally recursive, mirroring how the tree itself is built: to evaluate a BinaryOp, first evaluate its left child, then its right child, then combine with the operator. Evaluating a Number is the base case — it's already a value, nothing to recurse into.
"""

from mathforge.parser.ast_nodes import Number, BinaryOp
from mathforge.core.errors import UndefinedOperationError, InvalidOperandError


_OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}


def evaluate(node) -> float:
    """
    Recursively evaluate an AST node to a float result.

    Parameters
    ----------
    node : Number or BinaryOp
        Typically the root returned by Parser.parse(), but any sub-node can be evaluated independently too — useful for testing evaluate() without going through the full parser.

    Returns
    -------
    float

    Raises
    ------
    InvalidOperandError
        If node is not a Number or BinaryOp (e.g. None, or some other object accidentally passed in).
    UndefinedOperationError
        If a BinaryOp divides by a right-hand side that evaluates to zero.
    """
    if isinstance(node, Number):
        return node.value

    if isinstance(node, BinaryOp):
        left_value = evaluate(node.left)
        right_value = evaluate(node.right)

        if node.operator == "/":
            if right_value == 0:
                raise UndefinedOperationError("division by zero")
            return left_value / right_value

        operation = _OPERATIONS.get(node.operator)
        if operation is None:
            raise InvalidOperandError(f"unknown operator '{node.operator}'")
        return operation(left_value, right_value)

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