#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import time

class Stat():
    def __init__(self, balance):
        self.buffer = []
        self.trades = []
        self.initial_account_balance = balance
        self.final_account_balance = balance

        self.profit = []
        self.balance = []

        pd.options.display.mpl_style = 'default'
        plt.ion()

    def add_tick(self, tick):
        self.buffer.append(tick)

    def add_trade(self, trade):
        self.trades.append(trade)
        self.profit.append((trade.close_datetime, trade.profit))
        self.final_account_balance += trade.profit
        self.balance.append((trade.close_datetime, self.final_account_balance))

    def prepare_plot(self):
        ret = {}
        ret['prices'] = pd.DataFrame(self.buffer, columns=['datetime', 'buy', 'sell'])
        ret['prices'].set_index('datetime', inplace=True)

        ret['balance'] = pd.DataFrame(self.balance, columns=['datetime', 'balance'])
        ret['balance'].set_index('datetime', inplace=True)

        ret['profit'] = pd.DataFrame(self.profit, columns=['datetime', 'profit'])
        ret['profit'].set_index('datetime', inplace=True)

        return ret

    def __str__(self):
        profitable_trade_count = 0
        profitable_trade_profit = 0
        nonprofitable_trade_count = 0
        nonprofitable_trade_profit = 0
        trade_count = len(self.trades)
        for trade in self.trades:
            if trade.profit > 0:
                profitable_trade_count += 1
                profitable_trade_profit += trade.profit
            else:
                nonprofitable_trade_count += 1
                nonprofitable_trade_profit += trade.profit

        ret = "Statistics:\n"
        ret += "\tTrade count: " + str(trade_count) + "\n"
        ret += "\tProfitable trades:\n"
        ret += "\t\tCount: " + str(profitable_trade_count) + "\n"
        ret += "\t\tProfit: " + str(profitable_trade_profit) + "\n"
        ret += "\tNon-profitable trades \n"
        ret += "\t\tCount: " + str(nonprofitable_trade_count) + "\n"
        ret += "\t\tProfit: " + str(nonprofitable_trade_profit) + "\n"
        ret += "\tOverall profit: " + str(profitable_trade_profit + nonprofitable_trade_profit) + "\n"
        ret += "\tInitial account balance: " + str(self.initial_account_balance) + "\n"
        ret += "\tFinal account balance: " + str(self.final_account_balance) + "\n"
        return ret

    def plot(self, what=['balance'], show_trades=None):
        data = self.prepare_plot()

        fig, ax = plt.subplots(nrows=len(what)+1, sharex=True)

        # allways plot prices
        data['prices'].plot(ax=ax[0])

        # plot othe parameters
        for i, key in enumerate(what):
            if key in data:
                data[key].plot(ax=ax[i+1])
        if show_trades:
            for trade in self.trades:
                if show_trades == 'all':
                    for axe in ax:
                        axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='y', alpha=0.5, clip_on=False)
                elif show_trades == '+':
                    if trade.profit > 0:
                        for axe in ax:
                            axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='y', alpha=0.5, clip_on=False)
                elif show_trades == '-':
                    if trade.profit <= 0:
                        for axe in ax:
                            axe.axvspan(xmin=trade.open_datetime, xmax=trade.close_datetime, facecolor='y', alpha=0.5, clip_on=False)
        plt.show(block=True)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
