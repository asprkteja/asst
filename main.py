from operator import mul
from functools import reduce
from collections import deque
from time import time 

class Trade:
    '''Trade class to record Orders placed'''
    def __init__(self,quantity,indicator,price):
        self.timestamp = time()
        self.quantity = quantity
        self.indicator = indicator
        self.price = price
        
class CommonStock:
    '''Class to create a new common stock'''
    def __init__(self,symbol,price,last_dividend,par_value):
        self.symbol = symbol
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.price = price
        self.trades = deque()
    
    def __repr__(self):
        return '{} Common Stock\n  {:15}:{}\n  {:15}:{}\n  {:15}:{}'.format(self.symbol,
                                                                            'Price',self.price,
                                                                            'P/E Ratio',self.p_e_ratio(),
                                                                            'Dividend Yield',self.dividend_yield(),
                                                                            )

    def p_e_ratio(self,price=None):
        if price: self.update_price(price)
        try:
            res = round(self.price/self.last_dividend)
        except ZeroDivisionError:
            res = None
        return res

    def dividend_yield(self,price=None):
        if price: self.update_price(price)
        return round(self.last_dividend/self.price,2)
    
    def update_price(self,price):
        self.price = price

    def remove_old_trades(self):
        while self.trades and self.trades[0].timestamp < time() - 15 :
            self.trades.popleft()

    def record_trade(self,quantity):
        self.remove_old_trades()
        info = Trade(abs(quantity),'buy' if quantity>0 else 'sell',self.price)
        self.trades.append(info)
    
    def volume_weighted_stock_price(self):
        self.remove_old_trades()
        return sum([trade.quantity*trade.price for trade in self.trades])/sum([trade.quantity for trade in self.trades])


class PrefferedStock(CommonStock):
    '''class derived from CommonStock to implement dividend yield'''
    def __init__(self,symbol,price,last_dividend,fixed_dividend,par_value):
        super().__init__(symbol,price,last_dividend,par_value)
        self.fixed_dividend = fixed_dividend

    def dividend_yield(self, price=None):
        if price: self.update_price(price)
        return round(self.fixed_dividend * self.par_value / self.price,2)
    

class Index:
    '''class to construct index using stocks'''
    def __init__(self,stocks=[]):
        self.stocks = stocks
    
    def __add__(self,stock):
        self.stocks.append(stock)
        return self

    def __repr__(self):
        return '\nIndex:\n  {:20}:{}\n  {:20}:{}'.format('Composition',
                                                         ','.join([stock.symbol for stock in self.stocks]),
                                                         'All Share Index',
                                                         self.all_share_index()) 

    def all_share_index(self):
        return round(reduce(mul,[stock.price for stock in self.stocks])**(1/len(self.stocks)),2)