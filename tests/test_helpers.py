import pytest

from src.helpers import (format_percentage, get_percentage_diff, remove_negative_from_zero_number,
                         remove_zero_fractional, short_name)


@pytest.mark.parametrize(
    'name, expected',
    [
        pytest.param(
            'Газпром - привилегированные акции',
            'Газпром-П',
            id='should short'
        ),
        pytest.param(
            'Российские сети - акции привилегированные',
            'Российские сети-П',
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


@pytest.mark.parametrize(
    'number, expected',
    [
        pytest.param(123.45, '123.45', id='has_fractional'),
        pytest.param(123.00, '123', id='zero_fractional'),
    ])
def test_remove_zero_fractional(number, expected):
    assert remove_zero_fractional(number) == expected


@pytest.mark.parametrize(
    'number, expected',
    [
        pytest.param(-0.008, '-0.8%', id='negative'),
        pytest.param(0.089, '8.9%', id='positive'),
        pytest.param(0.0, '0.0%', id='zero'),
        pytest.param(-0.0, '-0.0%', id='negative_zero'),
        pytest.param(1.234, '123.4%', id='more_than_100%'),
    ])
def test_format_percentage(number, expected):
    assert format_percentage(number) == expected


@pytest.mark.parametrize(
    'number, expected',
    [
        pytest.param(-0.008, -0.008, id='negative'),
        pytest.param(123, 123, id='positive'),
        pytest.param(0.0, 0.0, id='zero_float'),
        pytest.param(-0.0, -0.0, id='negative_zero_float'),
        pytest.param(0, 0, id='zero_float'),
        pytest.param(-0, -0, id='negative_zero_int'),
    ])
def test_remove_negative_from_zero_number(number, expected):
    assert remove_negative_from_zero_number(number) == expected
