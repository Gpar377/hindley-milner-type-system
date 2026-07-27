from typing import Dict
from .types import Type, TypeVar, TypeCon

# A substitution is a mapping from TypeVar names to Type
Sub = Dict[str, Type]

def compose_sub(s1: Sub, s2: Sub) -> Sub:
    """Compose two substitutions: s1 . s2"""
    res = {k: v.apply(s1) for k, v in s2.items()}
    res.update(s1)
    return res

def occurs_check(tvar: TypeVar, t: Type) -> bool:
    """Check if the type variable tvar occurs in type t (occurs check)."""
    if isinstance(t, TypeVar):
        return tvar.name == t.name
    elif isinstance(t, TypeCon):
        return any(occurs_check(tvar, sub_t) for sub_t in t.types)
    return False

def unify(t1: Type, t2: Type) -> Sub:
    """Unify two types. Returns a substitution matching them or raises TypeError."""
    if isinstance(t1, TypeVar):
        return bind_var(t1, t2)
    elif isinstance(t2, TypeVar):
        return bind_var(t2, t1)
    elif isinstance(t1, TypeCon) and isinstance(t2, TypeCon):
        if t1.name != t2.name or len(t1.types) != len(t2.types):
            raise TypeError(f"Type mismatch: {t1} vs {t2}")
        sub = {}
        for ta, tb in zip(t1.types, t2.types):
            s = unify(ta.apply(sub), tb.apply(sub))
            sub = compose_sub(s, sub)
        return sub
    raise TypeError(f"Cannot unify: {t1} and {t2}")

def bind_var(tvar: TypeVar, t: Type) -> Sub:
    """Bind type variable to type, raising an error if it occurs check fails."""
    if isinstance(t, TypeVar) and tvar.name == t.name:
        return {} # Identity substitution
    if occurs_check(tvar, t):
        raise TypeError(f"Occurs check failed: type variable '{tvar}' would create recursive type in '{t}'")
    return {tvar.name: t}
