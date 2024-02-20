import unittest
from main import *
from random import randint
from time import sleep

inp = '''TEA Common 0 100
POP Common 8 100
ALE Common 23 60
GIN Preferred 8 0.02 100
JOE Common 13 250'''

inp = list(map(lambda x:tuple(x.split(' ')), inp.split('\n')))

def create(info):
    args = map(float,info[2:])
    return CommonStock(info[0],randint(1,100),*args) if info[1]=='Common' else PrefferedStock(info[0],randint(1,100),*args)

stocks = [create(stock_info) for stock_info in inp]
print('\n'.join([str(stock) for stock in stocks]))

gbce_index = Index(stocks)
print(gbce_index)

class Teststocks(unittest.TestCase):
    
    def get_common_stock(self):
        common_stock = CommonStock(symbol='ABC',price=10,last_dividend=2,par_value=100)
        return common_stock
    
    def get_preffered_stock(self):
        preffered_stock = PrefferedStock(symbol='DEF',price = 25,last_dividend=4,fixed_dividend=0.1,par_value=200)
        return preffered_stock
    
    def test_p_e_ratio(self):
        stock = self.get_common_stock()
        p_e_ratio = stock.p_e_ratio()
        self.assertEqual(p_e_ratio,5)
        print('\nP/E ratio test passed')

        stock.last_dividend = 0
        p_e_ratio = stock.p_e_ratio()
        self.assertEqual(p_e_ratio,None)
        print('division by 0 handled correctly')

    def test_dividend_yield(self):
        div_yield = self.get_common_stock().dividend_yield()
        self.assertEqual(div_yield,0.2)
        print('\nDividend Yield test passed for common stock')

        div_yield = self.get_preffered_stock().dividend_yield()
        self.assertEqual(div_yield,0.8)
        print('Dividend Yield test passed for preferred stock')
    
    def test_record_trade(self):
        stock = self.get_common_stock()
        stock.record_trade(-5)
    
        self.assertEqual(stock.trades[0].quantity,5)
        self.assertEqual(stock.trades[0].indicator,'sell')
        self.assertEqual(stock.trades[0].price,10)
        print('\nTrades recording successful')
        sleep(5)
        stock.update_price(20)
        stock.record_trade(5)
        self.assertEqual(stock.volume_weighted_stock_price(),15)
        print('volume weighted price is working')

        sleep(11)
        stock.update_price(40)
        stock.record_trade(15)
        self.assertEqual(stock.volume_weighted_stock_price(),35)    
        print('trades before 15 seconds are removed successfully')

    def test_index_construction(self):
        gbce_index = Index()
        common_stock = self.get_common_stock()
        preferred_stock = self.get_preffered_stock()
        
        gbce_index = gbce_index + preferred_stock + common_stock
        print('\nindex constructed')

        self.assertEqual(gbce_index.all_share_index(),15.81)
        print('volume weighted average price computed correctly')
        

if __name__=='__main__':
    unittest.main()
