import unittest
from decimal import Decimal

from converter import centimeters_to_meters, format_meters


class ConverterTests(unittest.TestCase):
    def test_whole_centimeters(self) -> None:
        self.assertEqual(centimeters_to_meters("150"), Decimal("1.5"))

    def test_decimal_centimeters(self) -> None:
        self.assertEqual(centimeters_to_meters("12.5"), Decimal("0.125"))

    def test_zero(self) -> None:
        self.assertEqual(centimeters_to_meters("0"), Decimal("0"))

    def test_whitespace_is_trimmed(self) -> None:
        self.assertEqual(centimeters_to_meters(" 200 "), Decimal("2"))

    def test_empty_input_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "请输入厘米数"):
            centimeters_to_meters("   ")

    def test_non_number_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "有效数字"):
            centimeters_to_meters("abc")

    def test_negative_number_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "不能小于 0"):
            centimeters_to_meters("-1")

    def test_result_format_removes_trailing_zeros(self) -> None:
        self.assertEqual(format_meters(Decimal("1.5000")), "1.5")


if __name__ == "__main__":
    unittest.main()
