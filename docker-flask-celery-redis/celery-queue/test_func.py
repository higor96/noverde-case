import pytest

from tasks import get_tax


@pytest.mark.parametrize(
    "score, terms, result",
    [
        (750, 9, 0.058),
        (610, 12, 0.069),
        (830, 6, 0.047),
    ],
)
def test_get_tax(score, terms, result):
    assert get_tax(score, terms) == result