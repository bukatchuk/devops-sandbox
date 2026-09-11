import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.calc import rate, total  # noqa: E402


def test_known():
    assert rate("fast") == 3


def test_unknown():
    assert rate("нет такого") == 1


def test_total():
    assert total(["fast", "slow", "нет такого"]) == 5
