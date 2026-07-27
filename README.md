# Hindley-Milner Type System

A standalone, robust type checker demonstrating **Hindley-Milner (HM) type inference** built from scratch in Python. It parses a subset of a functional language supporting variables, let-polymorphism, lambda abstractions, and literals, dynamically inferring and validating types without requiring explicit type annotations.

## Features & Architecture

*   **Abstract Syntax Tree (AST):** Represents expression constructs:
    *   Variables (`Var`)
    *   Lambda abstraction (`Lam` - e.g. `\x -> body`)
    *   Application (`App` - applying function to argument)
    *   Let binding (`Let` - `let x = e1 in e2`)
    *   Literals (`Lit` - integers, booleans)
*   **Type Representation:**
    *   Type Variables (`TypeVar` - polymorphic identifiers like `a`, `b`)
    *   Type Constructors (`TypeCon` - primitives like `Int`, `Bool`, and functions `a -> b`)
    *   Polymorphic Schemes (`Scheme` - quantified types like `forall a. a -> a`)
*   **Unification Solver:** Matches type constructs and applies substitutions, including structural occurs-check safeguards to prevent infinite recursive types (e.g. `\x -> x x`).
*   **Let-Polymorphism:** Properly generalizes bound variables inside let definitions (`generalize` and `instantiate` routines), supporting polymorphic reuse across expressions.

## Getting Started

### Prerequisites

*   Python 3.10 or higher. No external libraries are required.

### Run CLI Type Checker

You can run the type check utility on functional expressions using:

```bash
python check.py --expr "let id = \x -> x in id 5"
```

Output:
```text
Parsed AST: Let(id, Lam(x, Var(x)), App(Var(id), Lit(5)))
Inferred Type: Int
```

### Run Type Inference Tests

Run the built-in test suite to verify let-polymorphism, occurs-checks, and error reporting:

```bash
python run_tests.py
```
