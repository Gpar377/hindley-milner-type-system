# Claude Code Guidelines - Hindley Milner Typechecker

## Project Overview
This repository contains a Hindley-Milner type inference engine and syntax validator implemented in TypeScript or Python.

## Technology Stack
*   **TypeScript** (Deno/Node.js) or **Python 3.10+**
*   **Build/Test Tools:** Pytest (Python) or Vitest (TypeScript)

## Coding Standards & Conventions
*   Represent substitution mapping as a clean map structure. Avoid mutation of substitutions; instead, compose them functionally using helper methods.
*   Enforce structural occurs-checks: raise descriptive compilation errors if a type variable tries to unify with a type containing itself (which would cause infinite types).
*   Add exhaustive unit tests checking both valid expressions (e.g., standard mapping) and invalid expressions (e.g., passing an integer to a boolean-expected parameter).

## Workflow Rules & Commands
*   **Run Inference Tests:** `pytest tests/` or `npm run test`
*   **Run Check Utility:** `python check.py --expr "let id = \x -> x in id 5"`
