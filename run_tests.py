import unittest
from src.ast import Var, App, Lam, Let, Lit
from src.types import TypeVar, TypeCon, Scheme
from src.env import TypeEnv
from src.inference import InferenceEngine, IntType, BoolType
from check import parse_expr_string

# Configure a testing environment
a = TypeVar("a")
b = TypeVar("b")
add_type = TypeCon("->", [IntType, TypeCon("->", [IntType, IntType])])
pair_type = TypeCon("->", [a, TypeCon("->", [b, TypeCon("Pair", [a, b])])])
select_type = TypeCon("->", [BoolType, TypeCon("->", [a, TypeCon("->", [a, a])])])

TEST_ENV = TypeEnv({
    "add": Scheme([], add_type),
    "pair": Scheme(["a", "b"], pair_type),
    "select": Scheme(["a"], select_type)
})

class TestHMInference(unittest.TestCase):
    def test_literals(self):
        engine = InferenceEngine()
        
        _, t1 = engine.infer(TEST_ENV, Lit(5))
        self.assertEqual(str(t1), "Int")

        _, t2 = engine.infer(TEST_ENV, Lit(True))
        self.assertEqual(str(t2), "Bool")

    def test_identity(self):
        engine = InferenceEngine()
        expr = parse_expr_string("\\x -> x")
        _, t = engine.infer(TEST_ENV, expr)
        self.assertTrue(isinstance(t, TypeCon))
        self.assertEqual(t.name, "->")
        self.assertEqual(t.types[0].name, t.types[1].name)

    def test_let_polymorphism(self):
        engine = InferenceEngine()
        expr = parse_expr_string("let id = \\x -> x in pair (id 5) (id True)")
        _, t = engine.infer(TEST_ENV, expr)
        self.assertEqual(str(t), "Pair Int Bool")

    def test_type_mismatch(self):
        engine = InferenceEngine()
        expr = parse_expr_string("select 5 True False")
        with self.assertRaisesRegex(TypeError, "Type mismatch: Bool vs Int"):
            engine.infer(TEST_ENV, expr)

    def test_occurs_check(self):
        engine = InferenceEngine()
        expr = parse_expr_string("\\x -> x x")
        with self.assertRaisesRegex(TypeError, "Occurs check failed"):
            engine.infer(TEST_ENV, expr)

if __name__ == "__main__":
    unittest.main()
