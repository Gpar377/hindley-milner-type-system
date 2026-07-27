from typing import Dict, Set
from .types import Scheme, Type

class TypeEnv:
    def __init__(self, env: Dict[str, Scheme] = None):
        self.env = env if env is not None else {}

    def ftv(self) -> Set[str]:
        vars = set()
        for s in self.env.values():
            vars.update(s.ftv())
        return vars

    def apply(self, sub) -> 'TypeEnv':
        return TypeEnv({k: s.apply(sub) for k, s in self.env.items()})

    def extend(self, name: str, scheme: Scheme) -> 'TypeEnv':
        new_env = self.env.copy()
        new_env[name] = scheme
        return TypeEnv(new_env)

    def lookup(self, name: str) -> Scheme:
        if name in self.env:
            return self.env[name]
        raise TypeError(f"Unbound variable: {name}")

    def __repr__(self):
        return str(self.env)
