from decimal import Decimal, InvalidOperation


def centimeters_to_meters(raw_value: str) -> Decimal:
    """Convert a centimeter value entered by the user into meters."""
    text = raw_value.strip()
    if not text:
        raise ValueError("请输入厘米数。")

    try:
        centimeters = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("请输入有效数字，例如 150 或 12.5。") from exc

    if not centimeters.is_finite():
        raise ValueError("厘米数必须是有限数字。")
    if centimeters < 0:
        raise ValueError("厘米数不能小于 0。")

    return centimeters / Decimal("100")


def format_meters(meters: Decimal) -> str:
    """Format a decimal without unnecessary trailing zeros."""
    if meters == 0:
        return "0"
    return format(meters.normalize(), "f")
