def calculate_sip(investment, rate, months):
    total_amount = 0
    total_interest = 0
    print(f"{'Month':^5}|{'Investment':^15}|{'Interest':^15}|{'Total Amount':^15}")
    print("-" * 55)

    for month in range(1, months + 1):
        total_amount += investment
        interest = total_amount * (rate / 12 / 100)
        total_amount += interest
        total_interest += interest
        
        print(f"{month:^5}|Rs.{investment:^14,.2f}|Rs.{interest:^14,.2f}|Rs.{total_amount:^14,.2f}")
    
    return total_amount, total_interest

# Get user input
investment_amount = float(input("Enter the monthly investment amount: Rs."))
annual_rate = float(input("Enter the annual interest rate (%): "))
time_input = input("Enter the time period (format: number followed by 'm' for months or 'y' for years, e.g., '3m' or '2y'): ")

# Parse time input
if time_input.endswith('m'):
    time_period = int(time_input[:-1])
elif time_input.endswith('y'):
    time_period = int(time_input[:-1]) * 12
else:
    print("Invalid time format. Please use 'm' for months or 'y' for years.")
    exit()

# Calculate and display results
final_amount, total_interest = calculate_sip(investment_amount, annual_rate, time_period)
print("-" * 55)

# Calculate and display summary
total_invested = investment_amount * time_period
returns = final_amount - total_invested

print("\nSummary:")
print(f"Total Amount Invested: Rs.{total_invested:,.2f}")
print(f"Total Returns: Rs.{returns:,.2f}")
print(f"Total Interest Earned: Rs.{total_interest:,.2f}")
print(f"Final Total Amount: Rs.{final_amount:,.2f}")
print(f"Overall Return: {(returns/total_invested)*100:.2f}%")