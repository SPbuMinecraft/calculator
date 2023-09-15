import sys
sys.path.append('./server')

from interpreter import safe_eval


def test_parsing_trash():
    assert safe_eval("qwerty&8/'")[0] == False


def test_parsing_empty():
    assert safe_eval("")[0] == False


def test_parsing_brackets():
    #    assert formula_parsing("()")[0] == False
    assert safe_eval("())")[0] == False
    assert safe_eval("(")[0] == False
    assert safe_eval("12 + ) 8 ()")[0] == False
    assert safe_eval("(123 + 321))")[0] == False


def test_parsing_equation():
    assert safe_eval("2 * 3 = 6")[0] == False


def test_parsing_extra_symbols():
    assert safe_eval("3 + 7 * 5 / 3 - ")[0] == False


def test_parsing_unary_ops():
    assert safe_eval("-4")[1] == -4
    assert safe_eval("--4")[1] == 4
    assert safe_eval("+4")[1] == 4
    assert safe_eval("+-4")[1] == -4
