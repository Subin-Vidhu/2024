def calculate_sip(investment, rate, months):
    total_amount = 0
    print(f"{'Month':^5}|{'Investment':^15}|{'Interest':^15}|{'Total Amount':^15}")
    print("-" * 55)

    for month in range(1, months + 1):
        total_amount += investment
        interest = total_amount * (rate / 12 / 100)
        total_amount += interest
        
        print(f"{month:^5}|${investment:^14,.2f}|${interest:^14,.2f}|${total_amount:^14,.2f}")
    
    return total_amount

# Get user input
investment_amount = float(input("Enter the monthly investment amount: $"))
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
final_amount = calculate_sip(investment_amount, annual_rate, time_period)
print("-" * 55)
print(f"\nFinal Total Amount after {time_period} months: ${final_amount:,.2f}")