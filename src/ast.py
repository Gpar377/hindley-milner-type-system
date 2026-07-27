class AST:
    pass

class Var(AST):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"

class App(AST):
    def __init__(self, fn: AST, arg: AST):
        self.fn = fn
        self.arg = arg

    def __repr__(self):
        return f"App({self.fn}, {self.arg})"

class Lam(AST):
    def __init__(self, var: str, body: AST):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"Lam({self.var}, {self.body})"

class Let(AST):
    def __init__(self, var: str, defn: AST, body: AST):
        self.var = var
        self.defn = defn
        self.body = body

    def __repr__(self):
        return f"Let({self.var}, {self.defn}, {self.body})"

class Lit(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Lit({self.value})"
