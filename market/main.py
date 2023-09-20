from kite_trade import *
import time
import webbrowser

def is_correct_credentials(user_id, password):
    # Change these values to your actual credentials.
    CORRECT_ID = "eagle electrical"
    CORRECT_PASS = "eagle@168"


    return user_id == CORRECT_ID and password == CORRECT_PASS

# Prompt user for ID and password
user_id = input("Enter your ID: ")
password = input("Enter your password: ")

if is_correct_credentials(user_id, password):
    user_id = input("user_id: ")       # Login Id
    password = input("user pass: ")

    enctoken = input("user twofa: ")
    kite = KiteApp(enctoken=enctoken)

    def place_stop_loss_order(symbol, quantity, transaction_type, stop_price):
        order_info = kite.place_order(
            variety=kite.VARIETY_REGULAR,  # Fixed typo here
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=kite.ORDER_TYPE_SLM,
            product=kite.PRODUCT_NRML,
            trigger_price=stop_price,
            price=0  # Set price as 0 for stop-loss orders
        )
        return order_info

    def place_stop_profit_order(symbol, quantity, transaction_type, profit_price):
        order_info = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=kite.ORDER_TYPE_SL,
            product=kite.PRODUCT_NRML,
            trigger_price=profit_price,
            price=0  # Set price as 0 for stop-profit orders
        )
        return order_info

    def check_pending_orders(symbol):
        orders = kite.get_pending_orders()
        for order in orders:
            if order["tradingsymbol"] == symbol:
                print(f"Pending {order['transaction_type']} order exists for {symbol}. Skipping new orders.")
                return True
        return False

    # Example usage
    stock_symbol = input("Enter the stock symbol: ")
    order_quantity = input("Enter quantity of shares: ")
    stop_loss_price = float(input("Enter the stop-loss price: "))
    stop_profit_price = float(input("Enter the stop-profit price: "))

    while True:
        current_price = kite.get_market_price(stock_symbol)
        print(f"Current price of {stock_symbol}: {current_price}")

        pending_orders_exist = check_pending_orders(stock_symbol)
        if pending_orders_exist:
            print("Pending orders exist. Skipping new orders.")
            break

        if current_price <= stop_loss_price:
            print(f"Selling {stock_symbol} due to stop-loss trigger at price {current_price}")
            place_stop_loss_order(stock_symbol, order_quantity, kite.TRANSACTION_TYPE_SELL, stop_loss_price)
            break
        elif current_price >= stop_profit_price:
            print(f"Selling {stock_symbol} due to stop-profit trigger at price {current_price}")
            place_stop_profit_order(stock_symbol, order_quantity, kite.TRANSACTION_TYPE_SELL, stop_profit_price)
            break

        time.sleep(1)  # Pause for 1 second before checking the market value again
else:
    # Open another python file (or execute another function) if credentials are incorrect
    with open("second.py", 'r') as f:
        exec(f.read())
