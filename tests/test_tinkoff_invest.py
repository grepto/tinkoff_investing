from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from pytz import UTC

from src.tinkoff_invest import get_yesterday_candle, get_instrument_change

candels = [
    {'figi': 'BBG0047315Y7', 'interval': 'day', 'o': 214.55, 'c': 214.98, 'h': 215.99, 'l': 213.79, 'v': 298619,
     'time': datetime(2019, 11, 13, 7, 0)},
    {'figi': 'BBG0047315Y7', 'interval': 'day', 'o': 215.44, 'c': 215.44, 'h': 215.44, 'l': 215.44, 'v': 463,
     'time': datetime(2019, 11, 14, 7, 0, )}]


@pytest.fixture
def get_candles(mocker):
    return mocker.patch('src.tinkoff_invest.get_candles')


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
