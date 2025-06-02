from collections import deque
import random
import math

# FIFO queue for investments, each element: [buy_price, amount]
investments = deque()
day = 0
day_overview = []  # List to store daily transaction messages
user_money = 1000.00  # User starting money
user_stock = 0
stock_value = random.randint(5, 100)  # Generate initial random stock value

while day < 5:
    # Update stock value randomly between -50% and +50%
    stock_value = round(stock_value * (1 + random.uniform(-0.5, 0.5)), 2)
    print(f"Today's stock value: ${stock_value}")
    print(f"Your current money: ${user_money:.2f}")
    choice = input("Do you want to buy or sell? (Enter 'buy' or 'sell'): ").strip().lower()
    if choice == 'buy':
        # Calculate max stocks user can buy
        max_buy = math.floor(user_money / stock_value)
        if max_buy < 1:
            print("Not enough money to buy any stock.")
            continue
        amount = int(input(f"How much do you want to buy? (Enter '1'-'{max_buy}'): "))
        if 1 <= amount <= max_buy:
            user_money -= amount * stock_value  # Deduct money for purchase
            user_stock += amount  # Add to user's stock
            investments.append([stock_value, amount])  # Add purchase to FIFO queue
            msg = f"Bought {amount} shares at ${stock_value} each."
            print(msg)
            day_overview.append(msg)  # Log transaction
            day += 1  # Move to next day
        else:
            print("Invalid amount.")
    elif choice == 'sell':
        if user_stock < 1:
            print("No stock to sell.")
            continue
        max_sell = user_stock
        amount = int(input(f"How much do you want to sell? (Enter '1'-'{max_sell}'): "))
        if 1 <= amount <= max_sell:
            user_money += amount * stock_value  # Add money for sale
            user_stock -= amount  # Subtract from user's stock
            # FIFO: Remove sold stock from investments queue
            to_sell = amount
            while to_sell > 0 and investments: 
                buy_price, buy_amount = investments[0] #Queue get first value price and amount
                if buy_amount <= to_sell:   #Amount bought first less than amount selling
                    investments.popleft()  # Removes whole batch from queue
                    to_sell -= buy_amount 
                else:
                    investments[0][1] -= to_sell  # Remove part of first batch
                    to_sell = 0
            msg = f"Sold {amount} shares at ${stock_value} each."
            print(msg)
            day_overview.append(msg)  # Log transaction
            day += 1  # Move to next day
        else:
            print("Invalid amount.")
    else:
        print("Invalid choice. Please enter 'buy' or 'sell'.")

# If user has stock left at the end, sell all at next day's price
if user_stock > 0:
    stock_value = round(stock_value * (1 + random.uniform(-0.5, 0.5)), 2)
    user_money += user_stock * stock_value
    msg = f"Sold remaining {user_stock} shares at next day price ${stock_value}"
    print(msg)
    day_overview.append(msg)

# Print day overview at the end
print("\nDay Overview:")
for entry in day_overview:
    print(entry)

# Print total gain or loss
print("\nTotal Gain/Loss:")
gain_loss = round(user_money - 1000, 2)
if gain_loss > 0:
    print(f"The total capital gain is ${gain_loss}")
elif gain_loss == 0:
    print("The user broke even")
else:
    print(f"The total capital loss is ${gain_loss}")