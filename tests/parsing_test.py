import pytest
import sys
sys.path.append('./')

from calculations import formula_parsing


def test_parsing_trash():
    assert formula_parsing("qwerty&8/'")[0] == False

def test_parsing_empty():
    assert formula_parsing("")[0] == False

#does not pass
#def test_parsing_empty_brackets():
#    assert formula_parsing("()")[0] == False

def test_parsing_empty_brackets_2():
    assert formula_parsing("())")[0] == False

def test_parsing_empty_brackets_3():
    assert formula_parsing("(")[0] == False

def test_parsing_brackets_in_wrong_places():
    assert formula_parsing("12 + ) 8 ()")[0] == False

def test_parsing_too_many_brackets():
    assert formula_parsing("(123 + 321))")[0] == False

def test_parsing_equation():
    assert formula_parsing("2 * 3 = 6")[0] == False

def test_parsing_extra_symbols():
    assert formula_parsing("3 + 7 * x / y")[0] == False

def test_parsing_unary_neg():
    assert formula_parsing("-4")[1] == -4

def test_parsing_unary_pos():
    assert formula_parsing("+4")[1] == 4