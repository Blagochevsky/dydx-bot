from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits

if __name__ == "__main__":
    
    # Connect to client
    try:
        print("Connecting to Client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e)
        exit(1)
    
    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = abort_all_positions(client) 
        except Exception as e:
            print("Error connecting to client: ", e)
            exit(1)
            
    # Find Cointegrated Pairs
    if FIND_COINTEGRATED:
        
        # Construct Market Prices
        try:
            print("Fetching market prices, please allow 3 mins...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            exit(1)
            
        # Store Cointegrated Pairs
        try:
            print("Storing cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error saving cointegrated pairs: ", e)
            exit(1)
    
    # Run as always on
    while True:
            
        # Place trades for opening positions
        if MANAGE_EXITS:
            try:
                print("Managing exits...")
                manage_trade_exits(client)
            except Exception as e:
                print("Error managing exiting positions: ", e)
                exit(1)
            
        # Place trades for opening positions
        if PLACE_TRADES:
            try:
                print("Finding trading opportunities...")
                open_positions(client)
            except Exception as e:
                print("Error trading pairs: ", e)
                exit(1)
                
                
                """
                SOMETHING IS WRONG WITH THESE COINS: XTZ-USD, CELO-USD, EOS-USD
                Check this for 
                Error trading pairs:  'NoneType' object is not subscriptable 
                
                Claudio provided a solution to address the limitation on dydx 
                where certain coins require orders to be placed in quantities 
                that are factors of 10. His solution can be found in this link:
                https://www.udemy.com/course/dydx-pairs-trading-bot-build-in-python-running-in-the-cloud/learn/lecture/35540158#questions/18977196

                To summarize his solution:

                1. Claudio added an array called TOKEN_FACTOR_10 in the 
                constants.py file, which includes the list of tokens that 
                have the factor of 10 requirement.

                2. In the func_entry_file.py file, Claudio added the following
                code to the "GET SIZE" zone:

                ```
                # Get size
                base_quantity = 1 / base_price * USD_PER_TRADE
                quote_quantity = 1 / quote_price * USD_PER_TRADE

                # Adjust quantity for coins with factor of 10 requirement
                if base_market in TOKEN_FACTOR_10:
                    base_quantity = float(int(base_quantity / 10) * 10)
                if quote_market in TOKEN_FACTOR_10:
                    quote_quantity = float(int(quote_quantity / 10) * 10)
                ```

                This code checks if the base or quote market is in the
                TOKEN_FACTOR_10 array and, if so, adjusts the quantity to be 
                a factor of 10. Otherwise, the quantity remains as calculated 
                in the original version.
                """