"""
Verification script for sqrt(2) calculation
"""

import decimal
import math


def verify_sqrt2_accuracy(result_file):
    """
    Verify the accuracy of our sqrt(2) calculation by comparing with math.sqrt(2)
    and checking known digits.

    Args:
        result_file (str): Path to the file containing our sqrt(2) calculation

    Returns:
        bool: True if verification passes, False otherwise
    """
    # Read our calculated value
    with open(result_file, "r") as f:
        our_value_str = f.read().strip()

    # Convert to decimal
    our_value = decimal.Decimal(our_value_str)

    # Set high precision for comparison
    decimal.getcontext().prec = 10050

    # Calculate sqrt(2) using decimal module's method for comparison
    two = decimal.Decimal(2)
    reference_value = two.sqrt()

    # Compare the values
    print(f"Our calculated value: {our_value}")
    print(f"Reference value (decimal): {reference_value}")

    # Check if they match to at least 10000 decimal places
    # Convert both to strings and compare
    our_str = str(our_value)
    ref_str = str(reference_value)

    # Compare digit by digit
    match_count = 0
    for i, (our_digit, ref_digit) in enumerate(zip(our_str, ref_str)):
        if our_digit == ref_digit:
            match_count += 1
        else:
            print(
                f"First mismatch at position {i}: our='{our_digit}', reference='{ref_digit}'"
            )
            break

    print(f"Matching digits: {match_count}")

    # For 10000 decimal places, we should have 10002 characters (1 + 1 + 10000)
    # (including "1", ".", and 10000 decimal digits)
    expected_length = 10002
    actual_length = len(our_str)

    print(f"Expected length: {expected_length}")
    print(f"Actual length: {actual_length}")

    # Verification criteria
    min_matching_digits = 10000
    correct_length = (actual_length >= expected_length - 10) and (
        actual_length <= expected_length + 10
    )
    sufficient_match = match_count >= min_matching_digits

    print(f"\nVerification Results:")
    print(f"Correct length: {correct_length}")
    print(f"Sufficient matching digits: {sufficient_match}")

    return correct_length and sufficient_match


def main():
    """Main function to run verification"""
    print("Verifying sqrt(2) calculation accuracy...")
    print("=" * 50)

    result = verify_sqrt2_accuracy("sqrt_2_result.txt")

    if result:
        print("\nVERIFICATION PASSED: The calculation is accurate!")
    else:
        print("\nVERIFICATION FAILED: The calculation has issues.")


if __name__ == "__main__":
    main()
