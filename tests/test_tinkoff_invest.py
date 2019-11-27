from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from pytz import UTC

from src.tinkoff_invest import get_instrument_change, get_yesterday_candle, get_yesterday_market_result

portfolio = [
    {'figi': 'BBG004S686N0', 'ticker': 'BANEP', 'isin': 'RU0007976965', 'instrument_type': 'Stock', 'balance': 49.0,
     'blocked': None, 'lots': 49, 'expected_yield': {'currency': 'RUB', 'value': 4140.5},
     'average_position_price': {'currency': 'RUB', 'value': 1656.5}, 'average_position_price_no_nkd': None},
    {'figi': 'BBG004730RP0', 'ticker': 'GAZP', 'isin': 'RU0007661625', 'instrument_type': 'Stock', 'balance': 210.0,
     'blocked': None, 'lots': 21, 'expected_yield': {'currency': 'RUB', 'value': 7128.1},
     'average_position_price': {'currency': 'RUB', 'value': 220.86}, 'average_position_price_no_nkd': None},
    {'figi': 'BBG0047315Y7', 'ticker': 'SBERP', 'isin': 'RU0009029557', 'instrument_type': 'Stock', 'balance': 510.0,
     'blocked': None, 'lots': 51, 'expected_yield': {'currency': 'RUB', 'value': 9129.0},
     'average_position_price': {'currency': 'RUB', 'value': 196.6}, 'average_position_price_no_nkd': None},
    {'figi': 'BBG000BY2Y78', 'ticker': 'IVZ', 'isin': 'BMG491BT1088', 'instrument_type': 'Stock', 'balance': 13.0,
     'blocked': 13.0, 'lots': 13, 'expected_yield': {'currency': 'USD', 'value': 3.51},
     'average_position_price': {'currency': 'USD', 'value': 17.48}, 'average_position_price_no_nkd': None},
    {'figi': 'BBG005DXJS36', 'ticker': 'TCS', 'isin': 'US87238U2033', 'instrument_type': 'Stock', 'balance': 11.0,
     'blocked': None, 'lots': 11, 'expected_yield': {'currency': 'USD', 'value': -11.88},
     'average_position_price': {'currency': 'USD', 'value': 19.9}, 'average_position_price_no_nkd': None},
    {'figi': 'BBG00F0JX6G7', 'ticker': 'RU000A0JWWG0', 'isin': 'RU000A0JWWG0', 'instrument_type': 'Bond',
     'balance': 127.0, 'blocked': None, 'lots': 127, 'expected_yield': {'currency': 'RUB', 'value': 223.52},
     'average_position_price': {'currency': 'RUB', 'value': 798.9},
     'average_position_price_no_nkd': {'currency': 'RUB', 'value': 786.08}},
    {'figi': 'BBG00GK399S6', 'ticker': 'RU000A0JXQ93', 'isin': 'RU000A0JXQ93', 'instrument_type': 'Bond',
     'balance': 37.0, 'blocked': None, 'lots': 37, 'expected_yield': {'currency': 'RUB', 'value': 217.98},
     'average_position_price': {'currency': 'RUB', 'value': 879.35},
     'average_position_price_no_nkd': {'currency': 'RUB', 'value': 871.07}},
    {'figi': 'BBG005DXDPK9', 'ticker': 'FXGD', 'isin': 'IE00B8XB7377', 'instrument_type': 'Etf', 'balance': 184.0,
     'blocked': None, 'lots': 184, 'expected_yield': {'currency': 'RUB', 'value': -2403.2},
     'average_position_price': {'currency': 'RUB', 'value': 657.2}, 'average_position_price_no_nkd': None},
    {'figi': 'BBG0013HGFT4', 'ticker': 'USD000UTSTOM', 'isin': None, 'instrument_type': 'Currency', 'balance': 2.83,
     'blocked': 0.15, 'lots': 0, 'expected_yield': {'currency': 'RUB', 'value': -1.84},
     'average_position_price': {'currency': 'RUB', 'value': 64.66}, 'average_position_price_no_nkd': None}
]

candels = [
    {'figi': 'BBG0047315Y7', 'interval': 'day', 'o': 214.55, 'c': 214.98, 'h': 215.99, 'l': 213.79, 'v': 298619,
     'time': datetime(2019, 11, 13, 7, 0)},
    {'figi': 'BBG0047315Y7', 'interval': 'day', 'o': 215.44, 'c': 215.44, 'h': 215.44, 'l': 215.44, 'v': 463,
     'time': datetime(2019, 11, 14, 7, 0, )}]


@pytest.fixture
def get_candles(mocker):
    return mocker.patch('src.tinkoff_invest.get_candles')


@pytest.fixture
def get_portfolio(mocker):
    return mocker.patch('src.tinkoff_invest.get_portfolio')


@pytest.fixture
def instrument_change_result(mocker):
    return mocker.patch('src.tinkoff_invest.get_instrument_change')


@freeze_time("2019-11-14 15:48:11")
def test_get_yesterday_candle(get_candles):
    yesterday = datetime.now() - timedelta(days=1)
    get_candles.return_value = candels
    yesterday_candle = get_yesterday_candle('test trash')

    assert yesterday_candle['time'].date() == yesterday.date()


@pytest.mark.parametrize(
    '_from, to, interval',
    [
        pytest.param(
            datetime(2019, 11, 1, 0, 0, 0, 0, UTC),
            datetime(2019, 11, 22, 23, 59, 59, 0, UTC),
            'day',
            id='several days'
        ),
        pytest.param(
            datetime(2019, 11, 22, 0, 0, 0, 0, UTC),
            datetime(2019, 11, 22, 23, 59, 59, 0, UTC),
            '5min',
            id='one day'
        ),
    ],
)
def test_get_instrument_change_period(get_candles, _from, to, interval):
    get_instrument_change(figi='test trash', _from=_from, to=to)

    get_candles.assert_called_once_with(
        figi='test trash',
        _from=_from,
        to=to,
        interval=interval
    )


def test_get_instrument_change_result(get_candles):
    get_candles.return_value = candels

    instrument_change = get_instrument_change(figi='test trash', _from=datetime(2019, 1, 1, 0, 0, 0, 0),
                                              to=datetime(2019, 1, 1, 0, 0, 0, 0))

    assert instrument_change == dict(
        open=candels[0]['o'],
        close=candels[-1]['c'],
        lo=min(candels, key=lambda x: x['l'])['l'],
        hi=max(candels, key=lambda x: x['h'])['h'],
        vol=sum([candle['v'] for candle in candels])
    )


@pytest.mark.parametrize(
    'currency, expected_portfolio_len',
    [
        pytest.param('RUB', 3, id='RUB instruments'),
        pytest.param('USD', 2, id='USD instruments'),
    ]
)
def test_get_yesterday_market_result_portfolio_currency_filtering(get_portfolio, currency, expected_portfolio_len):
    get_portfolio.return_value = portfolio
    yesterday_market_result = get_yesterday_market_result(currency)['instruments']

    assert len(yesterday_market_result) == expected_portfolio_len


@freeze_time("2019-11-14 15:48:11")
def test_get_yesterday_market_result_from_to_dates(get_portfolio, instrument_change_result):
    get_portfolio.return_value = portfolio[:1]
    instrument_change_result.return_value = dict(open=1, close=2, lo=3, hi=4, vol=5)
    get_yesterday_market_result('RUB')

    yesterday = datetime.now(UTC) - timedelta(days=1)
    _from = yesterday.replace(hour=0, minute=0, second=0, microsecond=1)
    to = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)

    instrument_change_result.assert_called_with(portfolio[:1][0]['figi'], _from, to)
