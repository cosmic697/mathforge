"""
mathforge/parser/ast_nodes.py

AST node types for the expression parser.

A "node" is one piece of the tree; a full parsed expression is a tree of these, rooted at whichever node represents the outermost operation. Number is a leaf (holds a value, no children). BinaryOp is an internal node (holds an operator plus two child nodes, which may themselves be Number or BinaryOp — this is what lets the tree represent arbitrarily nested expressions).
"""


class Number:
    """
    A leaf node representing a single numeric literal.

    Attributes
    ----------
    value : float
    """

    def __init__(self, value: float):
        self.value = value

    def __repr__(self) -> str:
        return f"Number({self.value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Number):
            return NotImplemented
        return self.value == other.value


class BinaryOp:
    """
    An internal node representing a binary operation (left OPERATOR right).

    Attributes
    ----------
    operator : str
        One of "+", "-", "*", "/".
    left : Number or BinaryOp
    right : Number or BinaryOp
    """

    def __init__(self, operator: str, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"BinaryOp({self.operator!r}, {self.left!r}, {self.right!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryOp):
            return NotImplemented
        return (
            self.operator == other.operator
            and self.left == other.left
            and self.right == other.right
        )