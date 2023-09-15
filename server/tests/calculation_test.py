import sys
sys.path.append('./server')

from interpreter import safe_eval


def test_calculation_add():
    assert safe_eval("2 + 3")[1] == 2 + 3
    assert safe_eval("3 + (-1)")[1] == 3 + (-1)


def test_calculation_sub():
    assert safe_eval("3 - 2")[1] == 3 - 2
    assert safe_eval("- 3 - 2")[1] == - 3 - 2


def test_calculation_mul():
    assert safe_eval("2 * 3")[1] == 2 * 3
    assert safe_eval("2 * (-3)")[1] == 2 * (-3)


def test_calculation_div():
    assert safe_eval("2 / 3")[1] == 2 / 3


def test_calculation_pow():
    assert safe_eval("2 ** 3")[1] == 2 ** 3
    assert safe_eval("2 ** (-3)")[1] == 2 ** (-3)


def test_calculation_operation_order():
    assert safe_eval("2 * (3 + 4)")[1] == 2 * (3 + 4)
    assert safe_eval("2 * 3 + 4 ** 2")[1] == 2 * 3 + 4 ** 2
    assert safe_eval("8 / 2 * (2 + 2)")[1] == 8 / 2 * (2 + 2)


def test_calculation_pow_zero():
    assert safe_eval("3 ** 0")[1] == 1


def test_calculation_div_zero():
    assert safe_eval("3 / 0")[0] == False
