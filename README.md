# pymath

A Python module that aggregates functions and constants from various mathematical modules, including support for custom numeric bases, hyperreal numbers, complex numbers, and symbolic computation.

## Features

### Base conversion

Supports positive and negative bases
Convert numbers to and from decimal
Arithmetic operations (plus, minus, times, divide, pow) in any base

### Mathematical constants

π, τ, e, PHI (golden ratio), Catalan, Zeta(2), Zeta(4), Glaisher, Kaprekar, and more

Degrees, radians, gradians, lemniscate constants, Apery constant

### Hyperreal helpers

ε (epsilon), ±∞, infinitesimal calculations

### Complex numbers

cmpx class for custom complex arithmetic with readable formatting

### Symbolic computation

Wrapper around sympy for symbols, expansion, derivatives, and integrals
Utilities

* constshelp() → list all float constants
* funcshelp() → list all functions
* help() → prints all functions and constants

## Installation

```bash
pip install pymath
```

(Or copy the Python file into your project folder.)

## Usage Examples

```python
from pymath import BaseP, BaseN, cmpx, Symbol, integrate


# Base conversion
b10 = BaseP(10)
print(b10.to_base(255))       # "255"
b2 = BaseP(2)
print(b2.to_base(10))         # "1010"

# Arithmetic in custom base
print(b10.plus("10", "25"))   # "35"

# Complex numbers
z1 = cmpx(3, 4)
z2 = cmpx(1, -2)
print(z1 + z2)                # "4 + 2I"

# Symbolic math
x = Symbol("x")
expr = x**2 + 2*x + 1
print(derivate(expr, x))      # 2*x + 2

# List constants and functions
help()
```

## Notes

* Designed for Python 3.1 or more
* Supports both portable Python (USB) and standard installations
* Fractional parts in base conversion are approximated up to a default precision of 10 digits
