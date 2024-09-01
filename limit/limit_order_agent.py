from trading_framework.execution_client import ExecutionClient,ExecutionException
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file        
        for order in self.orders:
            try:
                if (order['buy_or_sell_flag'] == 'buy' and price <= order['limit']):
                    self.execution_client.buy(product_id, order['amount'])
                    self.orders.remove(order)                
                elif (order['buy_or_sell_flag'] == 'sell' and price >= order['limit']):
                    self.execution_client.sell(product_id, order['amount'])
                    self.orders.remove(order)
            except ExecutionException as e: print(f"Failed to execute order: {e}")
                

    def add_order(self, buy_or_sell_flag: str, product_id: str, amount: int, limit: float):
        self.orders.append({
            'buy_or_sell_flag': buy_or_sell_flag,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        })