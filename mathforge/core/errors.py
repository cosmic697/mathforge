"""
mathforge/core/errors.py

Base exception hierarchy for mathforge

Every error mathforge raises should trace back to MahtForgeError so callers can do 'except MathForgeError' to catch anything the library raises, regardless of which module it came from

"""

class MathForgeError(Exception):
    """Base class for every exception raised by MathForge"""

class InvalidOperandError(MathForgeError , TypeError):
    """
    Raised when an operation receives an operand of the wrong type.
    """

class UndefinedOperationError(MathForgeError , ValueError):
    """
    raised when invalid operation is mathematically undefined like GCD(0,0)
    """

class DomainError(MathForgeError,ValueError):
    """
    Raised when the value is outside the domain of a function/object accept.
    """

class ConvergenceError(MathForgeError):
    """
    Raiswd when a iterative numerical method fails to converge
    """

class ParserError(MathForgeError,SyntaxError):
    """
    Raised for malformed input to the expression parser
    """