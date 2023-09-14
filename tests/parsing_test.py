import sys
sys.path.append('./')

from calculations import formula_parsing


def test_parsing_trash():
    assert formula_parsing("qwerty&8/'")[0] == False

def test_parsing_empty():
    assert formula_parsing("")[0] == False

def test_parsing_brackets():
#    assert formula_parsing("()")[0] == False
    assert formula_parsing("())")[0] == False
    assert formula_parsing("(")[0] == False
    assert formula_parsing("12 + ) 8 ()")[0] == False
    assert formula_parsing("(123 + 321))")[0] == False

def test_parsing_equation():
    assert formula_parsing("2 * 3 = 6")[0] == False

def test_parsing_extra_symbols():
    assert formula_parsing("3 + 7 * 5 / 3 - ")[0] == False

def test_parsing_unary_ops():
    assert formula_parsing("-4")[1] == -4
    assert formula_parsing("--4")[1] == 4
    assert formula_parsing("+4")[1] == 4
    assert formula_parsing("+-4")[1] == -4
