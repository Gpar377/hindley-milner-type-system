import pytest
from src.ast import Var, App, Lam, Let, Lit
from src.types import TypeVar, TypeCon, Scheme
from src.env import TypeEnv
from src.inference import InferenceEngine, IntType, BoolType
from check import parse_expr_string

# Configure a testing environment
# add : Int -> Int -> Int
# pair : a -> b -> Pair a b
# select : Bool -> a -> a -> a
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

def test_literals():
    engine = InferenceEngine()
    
    _, t1 = engine.infer(TEST_ENV, Lit(5))
    assert str(t1) == "Int"

    _, t2 = engine.infer(TEST_ENV, Lit(True))
    assert str(t2) == "Bool"

def test_identity():
    engine = InferenceEngine()
    # \x -> x
    expr = parse_expr_string("\\x -> x")
    _, t = engine.infer(TEST_ENV, expr)
    # Expected type: a1 -> a1
    assert isinstance(t, TypeCon)
    assert t.name == "->"
    assert t.types[0].name == t.types[1].name

def test_let_polymorphism():
    engine = InferenceEngine()
    # let id = \x -> x in pair (id 5) (id True)
    expr = parse_expr_string("let id = \\x -> x in pair (id 5) (id True)")
    _, t = engine.infer(TEST_ENV, expr)
    assert str(t) == "Pair Int Bool"

def test_type_mismatch():
    engine = InferenceEngine()
    # select 5 True False (select expects Bool as first argument, gets Int)
    expr = parse_expr_string("select 5 True False")
    with pytest.raises(TypeError, match="Type mismatch: Bool vs Int"):
        engine.infer(TEST_ENV, expr)

def test_occurs_check():
    engine = InferenceEngine()
    # \x -> x x (Self-application requires infinite recursive type)
    expr = parse_expr_string("\\x -> x x")
    with pytest.raises(TypeError, match="Occurs check failed"):
        engine.infer(TEST_ENV, expr)
