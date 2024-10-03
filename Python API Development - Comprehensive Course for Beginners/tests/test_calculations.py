import pytest
from app.calculations import add
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (2, 2, 4),
    (5, 1, 6),
    (-1, 1, 0),
    (-1, -1, -2)
])
def test_add(a, b, expected):
    assert add(a, b) == expected
# test_add()