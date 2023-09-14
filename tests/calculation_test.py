import sys
sys.path.append('./')

from calculations import formula_parsing


def test_calculation_add():
    assert formula_parsing("2 + 3")[1] == 2 + 3
    assert formula_parsing("3 + (-1)")[1] == 3 + (-1)

def test_calculation_sub():
    assert formula_parsing("3 - 2")[1] == 3 - 2
    assert formula_parsing("- 3 - 2")[1] == - 3 - 2

def test_calculation_mul():
    assert formula_parsing("2 * 3")[1] == 2 * 3
    assert formula_parsing("2 * (-3)")[1] == 2 * (-3)

def test_calculation_div():
    assert formula_parsing("2 / 3")[1] == 2 / 3

def test_calculation_pow():
    assert formula_parsing("2 ** 3")[1] == 2 ** 3
    assert formula_parsing("2 ** (-3)")[1] == 2 ** (-3)

def test_calculation_operation_order():
    assert formula_parsing("2 * (3 + 4)")[1] == 2 * (3 + 4)
    assert formula_parsing("2 * 3 + 4 ** 2")[1] == 2 * 3 + 4 ** 2
    assert formula_parsing("8 / 2 * (2 + 2)")[1] == 8 / 2 * (2 + 2)

def test_calculation_pow_zero():
    assert formula_parsing("3 ** 0")[1] == 1

def test_calculation_div_zero():
    assert formula_parsing("3 / 0")[0] == False