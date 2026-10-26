from decimal import Decimal, InvalidOperation


def _parse_non_negative(raw_value: str, unit_name: str) -> Decimal:
    text = raw_value.strip()
    if not text:
        raise ValueError(f"请输入{unit_name}数。")

    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("请输入有效数字，例如 150 或 12.5。") from exc

    if not value.is_finite():
        raise ValueError(f"{unit_name}数必须是有限数字。")
    if value < 0:
        raise ValueError(f"{unit_name}数不能小于 0。")

    return value


def centimeters_to_meters(raw_value: str) -> Decimal:
    """Convert a centimeter value entered by the user into meters."""
    return _parse_non_negative(raw_value, "厘米") / Decimal("100")


def meters_to_centimeters(raw_value: str) -> Decimal:
    """Convert a meter value entered by the user into centimeters."""
    return _parse_non_negative(raw_value, "米") * Decimal("100")


def format_decimal(value: Decimal) -> str:
    """Format a decimal without unnecessary trailing zeros."""
    if value == 0:
        return "0"
    return format(value.normalize(), "f")
