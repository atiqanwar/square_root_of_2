"""
Calculate the square root of 2 to 10,000 decimal places using the decimal module
"""

import decimal


def sqrt_2_high_precision(decimal_places):
    """
    Calculate square root of 2 to specified number of decimal places
    using Newton's method with high precision arithmetic.

    Args:
        decimal_places (int): Number of decimal places to calculate

    Returns:
        decimal.Decimal: Square root of 2 to specified precision
    """
    # Set precision higher than requested to account for calculation overhead
    decimal.getcontext().prec = decimal_places + 50

    # Use Newton's method: x_{n+1} = (x_n + 2/x_n) / 2
    # Start with initial guess of 1.5
    x = decimal.Decimal("1.5")
    two = decimal.Decimal("2")

    # Continue until convergence
    prev_x = decimal.Decimal("0")
    while abs(x - prev_x) > decimal.Decimal(10) ** (-decimal_places - 10):
        prev_x = x
        x = (x + two / x) / 2

    # Set precision to exactly what we need
    decimal.getcontext().prec = decimal_places + 10
    return +x  # The + operator applies the current precision


def main():
    """Main function to calculate and display sqrt(2) to 10,000 decimal places"""
    decimal_places = 10000

    print(f"Calculating square root of 2 to {decimal_places} decimal places...")

    # Calculate sqrt(2)
    result = sqrt_2_high_precision(decimal_places)

    # Format output
    result_str = str(result)

    # Print result with proper formatting
    print("Square root of 2 to 10,000 decimal places:")
    print(result_str)

    # Also save to file
    with open("sqrt_2_result.txt", "w") as f:
        f.write(result_str)

    print(f"\nResult also saved to 'sqrt_2_result.txt'")
    print(f"Total characters in result: {len(result_str)}")


if __name__ == "__main__":
    main()
