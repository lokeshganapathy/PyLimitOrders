from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient,ExecutionException


class CustomExecutionClient:
    def buy(self, product_id: str, amount: int):
        if amount <= 0: raise ExecutionException(f"Invalid amount specified {amount}")
        if product_id == None: raise ExecutionException(f"Invalid Product ID - {product_id}")
        print(f"Buying {amount} shares in {product_id}")
                    
    def sell(self, product_id: str, amount: int):
        if amount <= 0: raise ExecutionException(f"Invalid amount specified {amount}")
        if product_id == None: raise ExecutionException(f"Invalid Product ID - {product_id}")
        print(f"Selling {amount} shares in {product_id}")

if __name__ == "__main__":
    customexecLient = CustomExecutionClient()
    limitagent = LimitOrderAgent(customexecLient)
    limitagent.add_order('buy', 'IBM', 1000, 100) # Initializing accept order
    limitagent.on_price_tick('IBM', 99)  # Should buy order
    limitagent.on_price_tick('IBM', 101) # Should not buy order

