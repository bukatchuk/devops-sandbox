"""Минимальное приложение: нужно только чтобы пайплайну было что собирать и проверять."""


def rate(name: str, table: dict[str, int] | None = None) -> int:
    """Возвращает коэффициент по имени. Неизвестное имя — единица."""
    table = table or {"fast": 3, "slow": 1}
    return table.get(name, 1)


def total(names: list[str]) -> int:
    return sum(rate(n) for n in names)
