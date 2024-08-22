def compound_interest(principal, rate, time, n=1):
    """
    Calculate compound interest.

    Args:
        principal (float): Initial investment amount.
        rate (float): Interest rate (in decimal form, e.g., 4% = 0.04).
        time (int): Time period (in years).
        n (int, optional): Number of times interest is compounded per year. Defaults to 1.

    Returns:
        float: Compound interest amount.
    """
    return principal * (1 + rate / n) ** (n * time)

def main():
    print("Compound Interest Calculator")
    print("---------------------------")

    principal = float(input("Enter the principal amount: "))
    rate = float(input("Enter the interest rate (in %): ")) / 100
    time = int(input("Enter the time period (in years): "))
    n = int(input("Enter the number of times interest is compounded per year (default=1): ") or 1)

    interest = compound_interest(principal, rate, time, n)
    total_amount = principal + interest

    print(f"Compound Interest: ${interest:.2f}")
    print(f"Total Amount: ${total_amount:.2f}")

if __name__ == "__main__":
    main()