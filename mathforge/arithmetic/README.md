# Arithmetic Module

> The numerical foundation of the MathForge mathematical engine.

---

## Overview

The Arithmetic module provides the fundamental numerical objects, algorithms, and utilities used throughout MathForge.

Rather than exposing standalone mathematical functions, this module models mathematical concepts as reusable Python objects with intuitive interfaces.

Almost every future module—including Algebra, Calculus, Statistics, Linear Algebra, Numerical Methods, Geometry, and the Expression Parser—will depend on this module.

---

## Goals

The primary goals of this module are:

- Build mathematical objects using Object-Oriented Programming.
- Implement arithmetic algorithms from scratch whenever practical.
- Provide clean and intuitive APIs.
- Maintain modular and extensible architecture.
- Ensure correctness through testing.
- Serve as the numerical foundation of MathForge.

---

## Scope

This module is responsible for:

- Numerical objects
- Arithmetic operations
- Exact arithmetic
- High precision arithmetic
- Number theory utilities
- Numerical conversions
- Precision handling

This module is **not responsible** for:

- Symbolic algebra
- Matrix operations
- Statistics
- Graph plotting
- Geometry
- Calculus

---

## Planned Components

### Basic Numbers

- Fraction
- Decimal
- Percentage
- Ratio

### Complex Numbers

- ComplexNumber

### Precision

- Interval
- PrecisionContext
- ScientificNotation

### Large Numbers

- BigInteger
- BigDecimal

### Number Theory

- GCD
- LCM
- Prime Utilities
- Modular Arithmetic

### Advanced

- Quaternion
- Dual Number
- Symbolic Numbers

---

## Design Philosophy

MathForge models mathematics using objects.

Example:

```python
a = Fraction(1, 2)
b = Fraction(3, 4)

result = a + b
```

instead of

```python
result = add_fraction(a, b)
```

Objects own their own operations.

---

## Current Development Stage

**Version:** 0.1

Current focus:

- Fraction
- GCD
- LCM
- Testing

---

## Dependencies

Current:

- Python Standard Library
- math module

Future:

- mathforge.core
- mathforge.parser

---

## Status

🚧 Active Development