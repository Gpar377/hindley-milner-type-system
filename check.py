import argparse
import sys
from src.ast import AST, Var, App, Lam, Let, Lit
from src.types import Type, TypeVar, TypeCon, Scheme
from src.env import TypeEnv
from src.inference import InferenceEngine, IntType, BoolType

class Tokenizer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def error(self, msg):
        raise ValueError(f"Lexical error: {msg} at index {self.pos}")

    def next_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.text):
            return None

        char = self.text[self.pos]
        if char == '\\':
            self.pos += 1
            return ('LAMBDA', '\\')
        if char == '.' or (char == '-' and self.pos + 1 < len(self.text) and self.text[self.pos+1] == '>'):
            if char == '-':
                self.pos += 2
                return ('ARROW', '->')
            self.pos += 1
            return ('DOT', '.')
        if char == '=':
            self.pos += 1
            return ('EQUALS', '=')
        if char == '(':
            self.pos += 1
            return ('LPAREN', '(')
        if char == ')':
            self.pos += 1
            return ('RPAREN', ')')

        # Names / Primitives
        if char.isalpha() or char == '_':
            start = self.pos
            while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
                self.pos += 1
            val = self.text[start:self.pos]
            if val == 'let': return ('LET', 'let')
            if val == 'in': return ('IN', 'in')
            if val == 'True': return ('BOOL', True)
            if val == 'False': return ('BOOL', False)
            return ('ID', val)

        # Numbers
        if char.isdigit():
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            return ('INT', int(self.text[start:self.pos]))

        self.error(f"Unexpected character: {char}")

class Parser:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.next_token()

    def error(self, msg):
        raise ValueError(f"Parse error: {msg} (got: {self.current_token})")

    def consume(self, expected_type):
        if self.current_token and self.current_token[0] == expected_type:
            val = self.current_token[1]
            self.current_token = self.tokenizer.next_token()
            return val
        self.error(f"Expected token type: {expected_type}")

    def parse(self) -> AST:
        expr = self.parse_expr()
        if self.current_token is not None:
            self.error("Unexpected trailing tokens")
        return expr

    def parse_expr(self) -> AST:
        if not self.current_token:
            self.error("Unexpected end of input")
        
        tok_type = self.current_token[0]

        if tok_type == 'LAMBDA':
            self.consume('LAMBDA')
            var = self.consume('ID')
            # Support both '\x -> body' and '\x . body'
            if self.current_token and self.current_token[0] == 'ARROW':
                self.consume('ARROW')
            else:
                self.consume('DOT')
            body = self.parse_expr()
            return Lam(var, body)

        elif tok_type == 'LET':
            self.consume('LET')
            var = self.consume('ID')
            self.consume('EQUALS')
            defn = self.parse_expr()
            self.consume('IN')
            body = self.parse_expr()
            return Let(var, defn, body)

        return self.parse_app()

    def parse_app(self) -> AST:
        # Left-associative application: f x y -> App(App(f, x), y)
        expr = self.parse_atom()
        while self.current_token and self.current_token[0] in ('ID', 'INT', 'BOOL', 'LPAREN'):
            arg = self.parse_atom()
            expr = App(expr, arg)
        return expr

    def parse_atom(self) -> AST:
        tok_type = self.current_token[0]
        if tok_type == 'ID':
            return Var(self.consume('ID'))
        elif tok_type == 'INT':
            return Lit(self.consume('INT'))
        elif tok_type == 'BOOL':
            return Lit(self.consume('BOOL'))
        elif tok_type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expr()
            self.consume('RPAREN')
            return expr
        self.error("Expected an atom")

def parse_expr_string(expr_str: str) -> AST:
    tokenizer = Tokenizer(expr_str)
    parser = Parser(tokenizer)
    return parser.parse()

def main():
    parser = argparse.ArgumentParser(description="Hindley-Milner Type Inference Utility")
    parser.add_argument("--expr", type=str, required=True, help="Functional expression to type check")
    args = parser.parse_args()

    # Base Environment with primitive operations
    # e.g., (+) : Int -> Int -> Int
    a = TypeVar("a")
    func_add_type = TypeCon("->", [IntType, TypeCon("->", [IntType, IntType])])
    
    env = TypeEnv({
        "add": Scheme([], func_add_type),
        "id": Scheme(["a"], TypeCon("->", [a, a]))
    })

    try:
        ast_tree = parse_expr_string(args.expr)
        print(f"Parsed AST: {ast_tree}")
        
        engine = InferenceEngine()
        sub, t = engine.infer(env, ast_tree)
        print(f"Inferred Type: {t}")
    except Exception as e:
        print(f"Type check failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
