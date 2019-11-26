import pytest

from src.helpers import short_name, get_percentage_diff


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


def test_get_percentage_diff():
    assert get_percentage_diff(1656.5, 1748) == 0.055236945366737095
