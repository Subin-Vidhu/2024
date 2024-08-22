def calculate_sip(investment_amount, rate, time):
    """
    Calculate the total amount based on SIP details.

    Args:
    investment_amount (float): The monthly investment amount.
    rate (float): The annual interest rate (in decimal form, e.g., 12% = 0.12).
    time (int): The number of months.

    Returns:
    list: A list of dictionaries containing the month, investment, interest, and total amount.
    """
    total_amount = 0
    results = []

    for month in range(1, time + 1):
        investment = investment_amount
        interest = (investment_amount + total_amount) * (rate / 12)
        total_amount = total_amount + investment + interest
        results.append({
            'Month': month,
            'Investment': investment,
            'Interest': interest,
            'Total Amount': total_amount
        })

    return results


def print_sip_results(results):
    """
    Print the SIP results in a tabular format.

    Args:
    results (list): A list of dictionaries containing the SIP results.
    """
    print(f"{'Month':^10} | {'Investment':^15} | {'Interest':^10} | {'Total Amount':^15}")
    print("-" * 50)
    for result in results:
        print(f"{result['Month']:^10} | {result['Investment']:^15.2f} | {result['Interest']:^10.2f} | {result['Total Amount']:^15.2f}")


# Example usage:
investment_amount = 10000
rate = 0.12  # 12% annual interest rate
time = 12  # 12 months

results = calculate_sip(investment_amount, rate, time)
print_sip_results(results)