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
    """Main function to calculate and display sqrt(2) to a user-specified number of decimal places"""
    # Prompt the user for desired number of decimal places
    while True:
        user_input = input(
            "Enter number of decimal places (positive integer, default 10000): "
        ).strip()
        if user_input == "":
            decimal_places = 10000
            print("No input provided. Using default: 10000 decimal places.")
            break
        try:
            decimal_places = int(user_input)
            if decimal_places < 0:
                print("Please enter a non-negative integer.")
                continue
            # Warn if the request is very large
            if decimal_places > 200000:
                confirm = (
                    input(
                        f"You requested {decimal_places} digits. This may be slow and use a lot of memory. Continue? (y/N): "
                    )
                    .strip()
                    .lower()
                )
                if confirm not in ("y", "yes"):
                    print("Request cancelled. Please enter a smaller number.")
                    continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    print(f"Calculating square root of 2 to {decimal_places} decimal places...")

    # Calculate sqrt(2)
    result = sqrt_2_high_precision(decimal_places)

    # Format output
    result_str = str(result)

    # Print result with proper formatting
    print(f"Square root of 2 to {decimal_places} decimal places:")
    print(result_str)

    # Also save to file (use utf-8 encoding to avoid platform encoding issues)
    with open("sqrt_2_result.txt", "w", encoding="utf-8") as f:
        f.write(result_str)

    print("\nResult also saved to 'sqrt_2_result.txt'")
    print(f"Total characters in result: {len(result_str)}")


if __name__ == "__main__":
    main()
