def compound_interest_monthly(principal, rate, time, n, monthly_investment):
    """
    Calculate compound interest on monthly investments.

    Args:
        principal (float): Initial investment amount (not used in this case).
        rate (float): Interest rate (in decimal form, e.g., 12% = 0.12).
        time (int): Time period (in years).
        n (int): Number of times interest is compounded per year.
        monthly_investment (float): Monthly investment amount.

    Returns:
        float: Total amount after compound interest.
    """
    total_amount = 0
    for month in range(time * 12):
        total_amount = (total_amount + monthly_investment) * (1 + rate / n) ** (1 / n)
    return total_amount

def main():
    print("Compound Interest Calculator")
    print("---------------------------")

    monthly_investment = float(input("Enter the monthly investment amount: "))
    rate = float(input("Enter the interest rate (in %): ")) / 100
    time = int(input("Enter the time period (in years): "))
    n = int(input("Enter the number of times interest is compounded per year (default=1): ") or 1)

    total_amount = compound_interest_monthly(0, rate, time, n, monthly_investment)

    print(f"Total Amount: ${total_amount:.2f}")

if __name__ == "__main__":
    main()