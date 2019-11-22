from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time


from src.tinkoff_invest import get_yesterday_candle


candels = [
    {'figi': 'BBG0047315Y7', 'interval': 'day', 'o': 214.55, 'c': 214.98, 'h': 215.99, 'l': 213.79, 'v': 298619,
     'time': datetime(2019, 11, 13, 7, 0)},
    {'figi': 'BBG0047315Y7', 'interval': 'day', 'o': 215.44, 'c': 215.44, 'h': 215.44, 'l': 215.44, 'v': 463,
     'time': datetime(2019, 11, 14, 7, 0,)}]


@pytest.fixture
def get_candles(mocker):
    return mocker.patch('src.tinkoff_invest.get_candles')


@freeze_time("2019-11-14 15:48:11")
def test_get_yesterday_candle(get_candles):
    yesterday = datetime.now() - timedelta(days=1)
    get_candles.return_value = candels
    yesterday_candle = get_yesterday_candle('test trash')

    assert yesterday_candle['time'].date() == yesterday.date()
