"""计算器服务单元测试。"""

import pytest

from app.services.calculator import CalculatorService


class TestCalculatorAdd:
    """加法测试。"""

    def test_add_two_positive_numbers(self):
        """测试两个正数相加。"""
        assert CalculatorService.add(2, 3) == 5.0

    def test_add_negative_numbers(self):
        """测试负数相加。"""
        assert CalculatorService.add(-1, -2) == -3.0

    def test_add_floats(self):
        """测试浮点数相加。"""
        result = CalculatorService.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-9

    def test_add_zero(self):
        """测试加零。"""
        assert CalculatorService.add(5, 0) == 5.0


class TestCalculatorSubtract:
    """减法测试。"""

    def test_subtract_positive(self):
        assert CalculatorService.subtract(10, 3) == 7.0

    def test_subtract_negative_result(self):
        assert CalculatorService.subtract(3, 10) == -7.0


class TestCalculatorMultiply:
    """乘法测试。"""

    def test_multiply_positive(self):
        assert CalculatorService.multiply(4, 5) == 20.0

    def test_multiply_by_zero(self):
        assert CalculatorService.multiply(100, 0) == 0.0

    def test_multiply_negative(self):
        assert CalculatorService.multiply(-3, 7) == -21.0


class TestCalculatorDivide:
    """除法测试。"""

    def test_divide_positive(self):
        assert CalculatorService.divide(10, 2) == 5.0

    def test_divide_result_is_float(self):
        assert CalculatorService.divide(7, 2) == 3.5

    def test_divide_by_zero_raises(self):
        """测试除以零抛出异常。"""
        with pytest.raises(ZeroDivisionError, match="除数不能为零"):
            CalculatorService.divide(10, 0)


class TestCalculatorTypeValidation:
    """类型验证测试。"""

    @pytest.mark.parametrize("a, b", [
        ("hello", 1),
        (1, "world"),
        (None, 1),
        (1, [1, 2]),
    ])
    def test_invalid_types_raise_type_error(self, a, b):
        """测试非数字类型抛出 TypeError。"""
        with pytest.raises(TypeError, match="两个参数都必须是数字类型"):
            CalculatorService.add(a, b)
