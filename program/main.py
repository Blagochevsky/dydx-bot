from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits
from datetime import datetime
# from func_messaging import send_message
import traceback
import time

# Maximum number of attempts to make
max_attempts = 5

# MAIN FUNCTION
if __name__ == "__main__":

  # Message on start
  # send_message("Bot launch successful")

  # Connect to client
  try:
    print("Connecting to Client")
    client = connect_dydx()
  except Exception as e:
    print(f"\033[91mError connecting to client: {e}\033[0m")
    # send_message(f"Failed to connect to client {e}")
    exit(1)

  # Abort all open positions
  if ABORT_ALL_POSITIONS:
    try:
      print("Closing all positions")
      close_orders = abort_all_positions(client)
    except Exception as e:
      print(f"\033[91mError closing all positions: {e}\033[0m")
      # send_message(f"Error closing all positions {e}")
      exit(1)

  # Find Cointegrated Pairs
  if FIND_COINTEGRATED:

    # Construct Market Prices
    try:
      print("Fetching market prices, please allow 3 mins")
      df_market_prices = construct_market_prices(client)
    except Exception as e:
      print(f"\033[91mError constructing market prices: {e}\033[0m")
      # send_message(f"Error constructing market prices {e}")
      exit(1)

    # Store Cointegrated Pairs
    try:
      print("Storing cointegrated pairs")
      stores_result = store_cointegration_results(df_market_prices)
      if stores_result != "saved":
        print(f"\033[91mError saving cointegrated pairs\033[0m")
        exit(1)
    except Exception as e:
      print(f"\033[91mError saving cointegrated pairs: {e}\033[0m")
      # send_message(f"Error saving cointegrated pairs {e}")
      exit(1)

  # Run as always on
  while True:

    # Place trades for opening positions
    if MANAGE_EXITS:
      try:
        print(f"{datetime.now().strftime('%H:%M')} Managing exits")
        manage_trade_exits(client)
      except Exception as e:
        print(f"\033[91mError managing exiting positions: {e}\033[0m")
        traceback.print_exc()
        # send_message(f"Error managing exiting positions {e}")
        exit(1)

    # Place trades for opening positions
    if PLACE_TRADES:
      for attempt in range(max_attempts):
        try:
          print(f"{datetime.now().strftime('%H:%M')} Finding trading opportunities")
          open_positions(client)

          # If the request was successful, break the loop
          break
        except Exception as e:
          print(f"\033[91mError trading pairs: {e}\033[0m")
          traceback.print_exc()
          # send_message(f"Error opening trades {e}")

          # If the maximum number of attempts has been reached, exit
          if attempt == max_attempts - 1:
              exit(1)
          
          # Wait for a while before retrying
          time.sleep(10)
            