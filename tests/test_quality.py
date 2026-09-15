"""Тесты для опытов урока 08.07.

test_useful проверяет поведение; test_empty только «касается» кода,
ничего не утверждая, — на нём видно, что покрытие и проверка это разные вещи.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.calc import rate, total  # noqa: E402


def test_useful():
    assert total(["fast", "slow"]) == 4


def test_empty():
    # Ни одного утверждения: строки выполнены, поведение не проверено.
    rate("fast")
    rate("нет такого")
    total(["fast"])
