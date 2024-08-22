def calculate_sip(investment, rate, months):
    total_amount = 0
    for month in range(1, months + 1):
        if month > 1:
            total_amount += investment
        interest = total_amount * (rate / 12 / 100)
        total_amount += interest
        
        print(f"Month {month}:")
        print(f"Investment: ${investment:,.2f}")
        print(f"Interest: ${interest:,.2f}")
        print(f"Total Amount: ${total_amount:,.2f}")
        print()
    
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
print(f"Final Total Amount after {time_period} months: ${final_amount:,.2f}")