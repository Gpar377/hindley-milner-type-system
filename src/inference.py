from typing import Tuple
from .ast import AST, Var, App, Lam, Let, Lit
from .types import Type, TypeVar, TypeCon, Scheme
from .env import TypeEnv
from .solver import unify, compose_sub, Sub

# Primitive Types
IntType = TypeCon("Int", [])
BoolType = TypeCon("Bool", [])

class InferenceEngine:
    def __init__(self):
        self.var_counter = 0

    def new_type_var(self) -> TypeVar:
        """Generate a fresh type variable."""
        self.var_counter += 1
        return TypeVar(f"a{self.var_counter}")

    def instantiate(self, scheme: Scheme) -> Type:
        """Strip quantifiers from a scheme and replace with fresh type variables."""
        sub = {name: self.new_type_var() for name in scheme.vars}
        return scheme.type.apply(sub)

    def generalize(self, env: TypeEnv, t: Type) -> Scheme:
        """Quantify over free variables in t not bound in the environment."""
        vars = sorted(list(t.ftv() - env.ftv()))
        return Scheme(vars, t)

    def infer(self, env: TypeEnv, expr: AST) -> Tuple[Sub, Type]:
        """Infer type of an expression in a type environment."""
        if isinstance(expr, Lit):
            if isinstance(expr.value, bool):
                return {}, BoolType
            elif isinstance(expr.value, int):
                return {}, IntType
            raise TypeError(f"Unknown literal value: {expr.value}")

        elif isinstance(expr, Var):
            # Lookup variable in environment and instantiate its type scheme
            scheme = env.lookup(expr.name)
            return {}, self.instantiate(scheme)

        elif isinstance(expr, Lam):
            # Assign a fresh type variable to lambda parameter
            param_var = self.new_type_var()
            extended_env = env.extend(expr.var, Scheme([], param_var))
            
            sub, body_type = self.infer(extended_env, expr.body)
            func_type = TypeCon("->", [param_var.apply(sub), body_type])
            return sub, func_type

        elif isinstance(expr, App):
            # Create a fresh type variable representing function return type
            res_var = self.new_type_var()
            
            s1, fn_type = self.infer(env, expr.fn)
            s2, arg_type = self.infer(env.apply(s1), expr.arg)
            
            # Compose substitutions
            s3 = unify(fn_type.apply(s2), TypeCon("->", [arg_type, res_var]))
            total_sub = compose_sub(s3, compose_sub(s2, s1))
            return total_sub, res_var.apply(total_sub)

        elif isinstance(expr, Let):
            # Infer type of definition first
            s1, defn_type = self.infer(env, expr.defn)
            
            # Generalize it to support let-polymorphism
            env_after_defn = env.apply(s1)
            defn_scheme = self.generalize(env_after_defn, defn_type)
            
            # Extend environment and infer body
            extended_env = env_after_defn.extend(expr.var, defn_scheme)
            s2, body_type = self.infer(extended_env, expr.body)
            
            return compose_sub(s2, s1), body_type

        raise TypeError(f"Unsupported AST node: {expr}")
