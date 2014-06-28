#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import importlib
from datetime import datetime

from src.local_data import LocalData
from src.stat import Stat
from src.trade import Trade
from src.driver import Driver

class TestBrokerLocal():
    def __init__(self, account_balance, margin_rate, tick_source, account_currency="EUR"):
        self.account_id = None
        self.account_name = 'Local test'
        self.account_currency = account_currency
        self.margin_rate = margin_rate

        self.balance = account_balance
        self.margin_available = account_balance
        self.margin_used = 0.0

        self.open_orders = 0
        self.open_orders_list = []
        self.open_trades = 0
        self.open_trades_list = []

        self.realized_pl = 0
        self.unrealized_pl = 0

        self.tick_source = Driver.init_module_config(tick_source)

        self.stat = Stat(account_balance)
        self.last_tick = {}

        self.logger = logging.getLogger(__name__)

    def __str__(self):
        ret = "Local test broker"
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

    def get_tick_data(self, instrument):
        for tick in self.tick_source.get_tick_data(instrument):
            self.stat.add_tick(tick)
            self.last_tick[instrument] = tick

            # close finished sl/tp trades
            self.open_trades_list = self.close_finished_trades(self.open_trades_list)

            yield tick

    def open(self, instrument, volume, order_type='market', expiry=None, **args):  # price=None, lower_bound=None, upper_bound=None, sl=None, tp=None, ts=None):
        if order_type == 'market':
            if volume > 0:
                open_price = self.last_tick[instrument].buy
            elif volume < 0:
                open_price = self.last_tick[instrument].sell

            trade = Trade(instrument=instrument,
                          volume=volume,
                          open_price=open_price,
                          open_datetime=self.last_tick[instrument].datetime)
            trade_margin = (abs(volume) * open_price) * self.margin_rate
            if self.margin_available - trade_margin < 0:
                print("Not enough money to open the trade")
                return None
            else:
                self.margin_available -= trade_margin
                self.margin_used += trade_margin
                self.open_trades += 1
                self.open_trades_list.append(trade)
                return trade
        else:
            self.logger.warning("oreder_type is not 'market' - not implemented yet")

    def close(self, trade):
        if trade.volume > 0:
            close_price = self.last_tick[trade.instrument].sell
        elif trade.volume < 0:
            close_price = self.last_tick[trade.instrument].buy

        trade.close(close_price, self.last_tick[trade.instrument].datetime)
        trade_margin = (abs(trade.volume) * close_price) * self.margin_rate

        self.margin_available += trade_margin
        self.margin_used -= trade_margin

        # get profit
        pl = (trade.close_rate - trade.open_rate) * abs(trade.volume)
        self.realized_pl += pl
        self.balance += pl
        trade.set_profit(pl)

        self.stat.add_trade(trade)
        return trade

    def convert_currency(self, instrument, base_volume, rate=None):
        if rate:
            return base_volume * rate
        else:
            tick = self.get_tick_data(instrument)

            if base_volume > 0: # buy
                return tick.buy * base_volume
            else: # sell
                return tick.sell * abs(base_volume)

    def close_finished_trades(self, trades):
        """
        Checks for sl/tp out. This method simulates what the real broker does and must
        be called from model after processing each new tick..
        TODO: trailing stoploss
        Arguments:
            trades list of all trades the model has opened
        Returns:
            list of trades left open
        """
        left_trades = []
        for trade in trades:
            if trade.volume > 0:
                if trade.sl:
                    if self.last_tick[trade.instrument] <= trade.sl:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
                if self.tp:
                    if self.last_tick[trade.instrument] >= trade.tp:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
            else:
                if trade.sl:
                    if self.last_tick[trade.instrument] >= trade.sl:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
                if self.tp:
                    if self.last_tick[trade.instrument] <= trade.tp:
                        self.close(trade)
                    else:
                        left_trades.append(trade)
        return left_trades

    def get_account(self):
        """Does nothing in local implementation
        """
        None

    def get_account_information(self):
        """Does nothing in local implementation
        """
        None

    def get_open_trades(self):
        return []

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
