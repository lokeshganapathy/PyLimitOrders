import unittest
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionException


class CustomExecutionClient:
    def __init__(self):
        self.orders = []

    def buy(self, product_id: str, amount: int):
        if amount <= 0: raise ExecutionException(f"Invalid amount specified {amount}")  
        if product_id == None: raise ExecutionException(f"Invalid Product ID - {product_id}")          
        self.orders.append(('buy', product_id, amount))

    def sell(self, product_id: str, amount: int):
        if amount <= 0: raise ExecutionException(f"Invalid amount specified {amount}")
        if product_id == None: raise ExecutionException(f"Invalid Product ID - {product_id}")
        self.orders.append(('sell', product_id, amount))


class TestLimitOrderAgent(unittest.TestCase):

    def setUp(self):
        self.execution_client = CustomExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_add_buy_order(self):
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0]['buy_sell_flag'], 'buy')
        self.assertEqual(self.agent.orders[0]['product_id'], 'IBM')
        self.assertEqual(self.agent.orders[0]['amount'], 1000)
        self.assertEqual(self.agent.orders[0]['limit'], 100)

    def test_add_sell_order(self):
        self.agent.add_order('sell', 'AAPL', 500, 150)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0]['buy_sell_flag'], 'sell')
        self.assertEqual(self.agent.orders[0]['product_id'], 'AAPL')
        self.assertEqual(self.agent.orders[0]['amount'], 500)
        self.assertEqual(self.agent.orders[0]['limit'], 150)

    def test_execute_buy_order(self):
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 99)
        self.assertEqual(len(self.agent.orders), 0)
        self.assertEqual(len(self.execution_client.orders), 1)
        self.assertEqual(self.execution_client.orders[0], ('buy', 'IBM', 1000))

    def test_execute_sell_order(self):
        self.agent.add_order('sell', 'AAPL', 500, 150)
        self.agent.on_price_tick('AAPL', 151)
        self.assertEqual(len(self.agent.orders), 0)
        self.assertEqual(len(self.execution_client.orders), 1)
        self.assertEqual(self.execution_client.orders[0], ('sell', 'AAPL', 500))

    def test_no_order_execution_when_price_not_met(self):
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 101)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(len(self.execution_client.orders), 0)

    def test_execution_exception_handling(self):
        self.agent.add_order('buy', 'IBM', -1000, 100)
        with self.assertLogs(level='INFO') as log:
            self.agent.on_price_tick('IBM', 99)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(len(self.execution_client.orders), 0)
        self.assertIn('INFO:root:Failed to execute order: Amount must be positive', log.output[0])

if __name__ == '__main__':
    unittest.main()
