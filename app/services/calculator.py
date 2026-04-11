"""计算器业务逻辑服务。"""

from typing import Union


class CalculatorService:
    """提供基础数学运算服务。"""

    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> float:
        """两数相加。

        Args:
            a: 第一个数
            b: 第二个数

        Returns:
            两数之和

        Raises:
            TypeError: 参数不是数字类型
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("两个参数都必须是数字类型")
        return float(a + b)

    @staticmethod
    def subtract(a: Union[int, float], b: Union[int, float]) -> float:
        """两数相减。"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("两个参数都必须是数字类型")
        return float(a - b)

    @staticmethod
    def multiply(a: Union[int, float], b: Union[int, float]) -> float:
        """两数相乘。"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("两个参数都必须是数字类型")
        return float(a * b)

    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> float:
        """两数相除。

        Raises:
            ZeroDivisionError: 除数为零
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("两个参数都必须是数字类型")
        if b == 0:
            raise ZeroDivisionError("除数不能为零")
        return float(a / b)
