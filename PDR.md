# Hindley-Milner Type System
A standalone type checker demonstrating Hindley-Milner (HM) type inference. It parses a small functional language AST supporting variables, let bindings, function application, abstractions, and basic primitives, dynamically inferring and validating types without needing explicit type annotations.

## Proposed Git Repo Name
`hindley-milner-typechecker`

## Architecture & Scope
*   **AST Definition:** Representation of functional expressions:
    *   Variables (`Var`)
    *   Application (`App` - applying function to argument)
    *   Abstraction (`Lam` - lambda terms `\x -> e`)
    *   Let Bindings (`Let` - `let x = e1 in e2`)
    *   Literals (`Lit` - integers, booleans)
*   **Type Representation:**
    *   Type Variables (`TypeVar` - representing polymorphic type parameters like `a`, `b`)
    *   Type Constructors (`TypeCon` - primitives like `Int`, `Bool`, and functions `a -> b`)
    *   Type Schemes (`Scheme` - representing quantified types `forall a. a -> a`)
*   **HM Inference Engine:**
    *   **Substitution:** Applying substitutions mapping type variables to concrete types across terms.
    *   **Unification:** The core logic matching and checking compatibility of two types. Generates equations and fails on type conflicts (occurs check).
    *   **Generalization:** Converting a type into a scheme by quantifying over all free variables not bound in the active typing environment.
    *   **Instantiation:** Stripping quantifiers from a scheme and replacing them with fresh type variables.

## Target Milestones
1. AST representation and basic Type/Scheme data structures.
2. Unification solver with occurs-check logic.
3. Type environment tracking and generalization routines.
4. Let-polymorphism type checking implementation.
5. Verification suite verifying classic functional expressions (e.g., identity, map, composition).
