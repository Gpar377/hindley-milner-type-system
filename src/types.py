from typing import List, Set

class Type:
    def ftv(self) -> Set[str]:
        """Return set of free type variables."""
        raise NotImplementedError

    def apply(self, sub) -> 'Type':
        """Apply substitution map to type."""
        raise NotImplementedError

class TypeVar(Type):
    def __init__(self, name: str):
        self.name = name

    def ftv(self) -> Set[str]:
        return {self.name}

    def apply(self, sub) -> Type:
        if self.name in sub:
            return sub[self.name]
        return self

    def __repr__(self):
        return self.name

class TypeCon(Type):
    def __init__(self, name: str, types: List[Type]):
        self.name = name
        self.types = types

    def ftv(self) -> Set[str]:
        vars = set()
        for t in self.types:
            vars.update(t.ftv())
        return vars

    def apply(self, sub) -> Type:
        return TypeCon(self.name, [t.apply(sub) for t in self.types])

    def __repr__(self):
        if self.name == "->":
            return f"({self.types[0]} -> {self.types[1]})"
        if not self.types:
            return self.name
        return f"{self.name} " + " ".join(map(str, self.types))

class Scheme:
    def __init__(self, vars: List[str], type: Type):
        self.vars = vars
        self.type = type

    def ftv(self) -> Set[str]:
        return self.type.ftv() - set(self.vars)

    def apply(self, sub) -> 'Scheme':
        # Remove quantified variables from substitution mapping
        sub = {k: v for k, v in sub.items() if k not in self.vars}
        return Scheme(self.vars, self.type.apply(sub))

    def __repr__(self):
        if not self.vars:
            return str(self.type)
        return f"forall " + " ".join(self.vars) + ". " + str(self.type)
