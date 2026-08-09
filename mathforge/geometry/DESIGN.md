# Geometry Module Design

## Purpose
Provides 2D geometric primitives and the measurements built on them.
Line depends on Point (needs two). Triangle depends on Point (needs
three, or three side lengths). Circle depends on Point (center) plus
a radius.

## Design Principles
Same as linear_algebra/DESIGN.md: object-oriented, encapsulation
(shape.area() not area(shape)), immutable, consistent API.

## Planned Structure
geometry/
point.py
line.py
triangle.py
circle.py

## Internal Dependencies
- Point: no dependencies
- Line: Point
- Triangle: Point
- Circle: Point

## Coding Standards
Same as other modules — type hints, docstrings, one class per file
(Point is the exception worth noting: Line/Triangle/Circle files
will each `from mathforge.geometry.point import Point`).