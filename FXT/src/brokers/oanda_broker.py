#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import sleep
from collections import namedtuple

import src.thirdparty.oandapy.oandapy as oandapy
from src.stat import Stat
from src.trade import Trade

Tick = namedtuple("Tick", "datetime buy sell")

class OandaBroker():
    def __init__(self, enviroment, username, access_token=None, rate_freq_ms=500):
        """
        :param enviroment: the environment for oanda's REST api, either 'sandbox', 'practice', or 'live'.
        :param username: username for Oanda broker
        :param access_token: a valid access token if you have one. This is required if the environment is not sandbox.
        :param rate_freq_ms: how often should be the server asked to get new rates in milliseconds. Default: 500
        """
        # connect to the broker
        self.oanda = oandapy.API(environment=enviroment, access_token=access_token)

        # get basic account info
        self.get_account(username=username)
        self.get_account_information()

        # rates streaming
        self.rate_freq = timedelta(milliseconds=rate_freq_ms)
        self.sleep_time = (rate_freq_ms / 1000.0) / 10.0
        self.last_tick_datetime = datetime.now()

        self.stat = Stat(self.balance)

    def __str__(self):
        ret = "OANDA broker"
        ret += "account id: " + str(self.account_id) + "\n"
        ret += "account name: " + str(self.account_name) + "\n"
        ret += "account currency: " + str(self.account_currency) + "\n"
        ret += "balance: " + str(self.balance) + "\n"
        ret += "margin available: " + str(self.margin_available) + "\n"
        ret += "margin used: " + str(self.margin_used) + "\n"
        ret += "margin rate:  " + str(self.margin_rate) + "\n"
        ret += "realized pl: " + str(self.realized_pl) + "\n"
        ret += "unrealized pl:  " + str(self.unrealized_pl) + "\n"
        return ret

    def _str2datetime(self, str_datetime):
        return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_tick_data(self, instrument):
        while(1):
            now = datetime.now()
            if now - self.last_tick_datetime >= self.rate_freq:
                self.last_tick_datetime = now
                response = self.oanda.get_prices(instruments=instrument[0] + "_" + instrument[1])
                t = response.get("prices")[0]
                yield Tick(self._str2datetime(t['time']), t['ask'], t['bid'])
            else:
                sleep(self.sleep_time) # don't let the CPU grind so much

    def open(self, instrument, volume, order_type='market', expiry=None, **args):  # price=None, lower_bound=None, upper_bound=None, sl=None, tp=None, ts=None):
        if expiry is None:
            expiry = datetime.now() + timedelta(days=1)
            expiry = expiry.isoformat("T") + "Z"

        response = self.oanda.create_order(self.account_id,
            instrument=instrument[0] + "_" + instrument[1],
            units=abs(volume),
            side='buy' if volume > 0 else 'sell',
            type='market',
            expiry=expiry,
            **{k:v for k, v in args.items() if v is not None}
        )

        if response['tradeOpened']:
            return Trade(instrument=instrument,
                         volume=volume,
                         open_price=response['price'],
                         margin_rate=self.margin_rate,
                         sl=response['tradeOpened']['stopLoss'],
                         tp=response['tradeOpened']['takeProfit'],
                         ts=response['tradeOpened']['trailingStop'],
                         id=response['tradeOpened']['id'],
                         open_datetime=self._str2datetime(response['time']))
        elif response['tradesClosed']:
            print("When opening trade, 'tradesClosed' returned. This is not implemented, careful!!!")
            return None
        elif response['tradeReduced']:
            print("When opening trade, 'tradeReduced' returned. This is not implemented, careful!!!")
            return None

    def close(self, trade):
        # try to close trade
        response = self.oanda.close_trade(self.account_id, trade.id)

        # if the trade was found
        if 'code' not in response:
            trade.close(response['price'], response['time'])
            trade.set_profit(response['profit'])
            self.balance += response['profit']
            self.stat.add_trade(trade)
        else:
            # try to close order
            response = self.oanda.close_order(self.account_id, trade.id)
            trade = None
        return trade


    def convert_currency(self, instrument, base_volume, rate=None):
        if rate:
            return base_volume * rate
        else:
            tick = self.get_tick_data(instrument).next()
            if base_volume > 0:
                return tick.buy * base_volume
            else:
                return tick.sell * abs(base_volume)

    def get_account(self, username):
        response = self.oanda.get_accounts(username=username)

        account = response.get("accounts")[0]
        self.account_id = account['accountId']
        self.account_name = account['accountName']
        self.account_currency = account['accountCurrency']
        self.margin_rate = account['marginRate']

    def get_account_information(self):
        response = self.oanda.get_account(account_id=self.account_id)

        self.balance = response['balance']
        self.margin_available = response['marginAvail']
        self.margin_used = response['marginUsed']

        self.open_orders = response['openOrders']
        self.open_trades = response['openTrades']

        self.realized_pl = response['realizedPl']
        self.unrealized_pl = response['unrealizedPl']

    def get_open_trades(self):
        response = self.oanda.get_trades(account_id=self.account_id)

        open_trades = []

        trades = response.get("trades")
        for trade in trades:
            volume = -trade['units'] if trade['side'] == 'sell' else trade['units']
            instrument = (trade['instrument'][:3], trade['instrument'][-3:])

            open_trades.append(Trade(instrument=instrument,
                                     volume=volume,
                                     open_price=trade['price'],
                                     margin_rate=self.margin_rate,
                                     id=trade['id'],
                                     sl=trade['stopLoss'],
                                     tp=trade['takeProfit'],
                                     ts=trade['trailingStop'],
                                     open_datetime=self._str2datetime(trade['time'])))

        open_trades.reverse()
        return open_trades

    def get_open_orders(self):
        pass

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
