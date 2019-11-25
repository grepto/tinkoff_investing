import pytest

from src.helpers import short_name

@pytest.mark.parametrize(
    'name, expected',
    [
        pytest.param(
            'Газпром - привилегированные акции',
            'Газпром-П',
            id='should short'
        ),
        pytest.param(
            'Группа ЛСР',
            'Группа ЛСР',
            id='should not short'
        ),
    ],
)
def test_short_name(name, expected):
    assert short_name(name) == expected
