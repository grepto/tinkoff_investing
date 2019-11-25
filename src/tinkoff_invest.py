import sys
from datetime import datetime, timedelta

from envparse import env
from openapi_client import openapi
from pytz import UTC

SECONDS_PER_DAY = 86400

env.read_envfile()

client = openapi.api_client(env('TINKOFF_TOKEN'))


def get_portfolio() -> dict:
    return client.portfolio.portfolio_get().payload.to_dict()['positions']


def get_instrument(figi: str) -> dict:
    return client.market.market_search_by_figi_get(figi=figi).payload.to_dict()


def get_candles(figi: str, _from: datetime, to: datetime, interval: str) -> list:
    return client.market.market_candles_get(figi=figi, _from=_from, to=to, interval=interval).payload.to_dict()[
        'candles']


def get_orderbook(figi: str, depth: int):
    return client.market.market_orderbook_get(figi=figi, depth=depth).payload.to_dict()


def get_yesterday_candle(figi: str) -> dict:
    """Get instrument daily yield"""

    now = datetime.now(tz=UTC)

    yesterday = now - timedelta(days=1)
    before_yesterday = yesterday - timedelta(days=1)

    _from = before_yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    to = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)

    candles = get_candles(figi=figi, _from=_from, to=to, interval='day')
    yesterday_candle = [candle for candle in candles if candle['time'].date() == yesterday.date()]

    if yesterday_candle:
        return yesterday_candle[0]


def get_instrument_change(figi: str, _from: datetime, to: datetime) -> dict:
    delta = to - _from
    interval = 'day' if delta.total_seconds() >= SECONDS_PER_DAY else '5min'

    candles = get_candles(figi=figi, _from=_from, to=to, interval=interval)

    open = candles[0]['o']
    close = candles[-1]['c']

    lo, hi, vol = sys.maxsize, 0, 0
    for l, h, v in ((candle['l'], candle['h'], candle['v']) for candle in candles):
        lo, hi = min(l, lo), max(h, hi)
        vol += v

    return dict(open=open, close=close, lo=lo, hi=hi, vol=vol)


if __name__ == '__main__':
    figi = 'BBG004S686N0'  # BANEP
