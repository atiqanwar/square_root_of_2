#!/usr/bin/env python3
"""
Calculate and verify the square root of 2 to a user-specified number of decimal places.

Behavior:
- Prompts the user for how many decimal places they want (default 10000).
- Computes sqrt(2) using Newton's method with the decimal module at high precision.
- Writes the result to "sqrt_2_result.txt" (UTF-8).
- Immediately verifies the written result by computing a reference sqrt(2) using
  the decimal module and comparing the digits exactly (no rounding).
- Reports success or the first mismatch position.

Notes:
- Very large requests are supported but may consume a lot of time and memory.
- The script uses ROUND_DOWN when producing the fixed-digit string so the output
  contains exactly the requested number of digits (no rounding up).
"""

from __future__ import annotations

import decimal
import os
import sys
import time
from decimal import ROUND_DOWN, Decimal

RESULT_FILENAME = "sqrt_2_result.txt"


def prompt_decimal_places(default: int = 10000) -> int:
    while True:
        try:
            user_input = input(
                f"Enter number of decimal places (non-negative integer, default {default}): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Exiting.")
            sys.exit(1)

        if user_input == "":
            print(f"No input provided. Using default: {default} decimal places.")
            return default

        try:
            n = int(user_input)
            if n < 0:
                print("Please enter a non-negative integer.")
                continue
            if n > 500000:
                confirm = (
                    input(
                        f"You requested {n} digits. This may be very slow and require a lot of memory. Continue? (y/N): "
                    )
                    .strip()
                    .lower()
                )
                if confirm not in ("y", "yes"):
                    print("Cancelled. Please enter a smaller number.")
                    continue
            return n
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def sqrt_2_high_precision(decimal_places: int, max_iterations: int = 10000) -> Decimal:
    """
    Compute sqrt(2) using Newton's method to at least `decimal_places` fractional digits.

    Returns a Decimal that has been quantized/truncated to the requested digits
    (but still as Decimal object).
    """
    if decimal_places == 0:
        # quick path
        return Decimal(2).sqrt()

    # Provide a safety margin for internal precision to avoid rounding errors
    working_prec = decimal_places + 30
    decimal.getcontext().prec = working_prec
    decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN

    two = Decimal(2)
    x = Decimal(1.5)  # initial guess
    prev_x = Decimal(0)

    # Convergence threshold (in Decimal relative terms)
    threshold = Decimal(10) ** (-(decimal_places + 10))

    iter_count = 0
    start_time = time.time()
    while True:
        iter_count += 1
        prev_x = x
        x = (x + two / x) / 2
        if abs(x - prev_x) <= threshold:
            break
        if iter_count >= max_iterations:
            raise RuntimeError(
                "Newton iteration did not converge within max iterations"
            )
        # occasional progress print for very long runs
        if iter_count % 1000 == 0:
            elapsed = time.time() - start_time
            print(f"Iteration {iter_count} elapsed {elapsed:.1f}s ...")

    # Truncate to exactly requested decimals without rounding up
    decimal.getcontext().prec = decimal_places + 10
    decimal.getcontext().rounding = ROUND_DOWN
    quant = Decimal(1).scaleb(-decimal_places)  # 1E-<decimal_places>
    x_trunc = x.quantize(quant, rounding=ROUND_DOWN)
    return x_trunc


def decimal_to_fixed_string(value: Decimal, decimal_places: int) -> str:
    """
    Convert Decimal to a fixed-point string with exactly decimal_places fractional digits.
    Uses ROUND_DOWN on the provided Decimal value (assumes it's already truncated).
    """
    if decimal_places == 0:
        # no fractional part
        return format(value.quantize(Decimal(1), rounding=ROUND_DOWN), "f")

    # Ensure quantization without rounding up
    quant = Decimal(1).scaleb(-decimal_places)
    v = value.quantize(quant, rounding=ROUND_DOWN)
    s = format(v, "f")

    # Guarantee there's a decimal point
    if "." not in s:
        s = s + "." + ("0" * decimal_places)
    else:
        int_part, frac_part = s.split(".")
        if len(frac_part) < decimal_places:
            frac_part = frac_part + ("0" * (decimal_places - len(frac_part)))
        elif len(frac_part) > decimal_places:
            frac_part = frac_part[:decimal_places]
        s = int_part + "." + frac_part
    return s


def write_result_to_file(text: str, filename: str = RESULT_FILENAME) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def verify_written_result(filename: str, decimal_places: int) -> bool:
    """
    Verify the content of filename matches Decimal(2).sqrt() to the requested digits.
    Returns True if they match exactly, False otherwise. On mismatch, prints the first
    mismatch location and context.
    """
    if not os.path.exists(filename):
        print("Result file not found for verification.")
        return False

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Compute reference using decimal at sufficient precision
    verify_prec = decimal_places + 40
    decimal.getcontext().prec = verify_prec
    decimal.getcontext().rounding = ROUND_DOWN
    reference = Decimal(2).sqrt()
    reference_trunc = reference.quantize(
        Decimal(1).scaleb(-decimal_places), rounding=ROUND_DOWN
    )
    ref_str = decimal_to_fixed_string(reference_trunc, decimal_places)

    # Normalize both strings (remove any leading/trailing spaces)
    ours = content.strip()
    ref = ref_str.strip()

    if ours == ref:
        print("Verification passed: written result matches reference exactly.")
        return True

    # Find first mismatch position
    min_len = min(len(ours), len(ref))
    mismatch_pos = None
    for i in range(min_len):
        if ours[i] != ref[i]:
            mismatch_pos = i
            break
    if mismatch_pos is None:
        # One is a prefix of the other
        mismatch_pos = min_len

    # Convert mismatch_pos into digit index (account for "1." prefix)
    print("Verification failed.")
    print(f"Length of written result: {len(ours)}")
    print(f"Length of reference result: {len(ref)}")
    print(f"First mismatch at index: {mismatch_pos}")
    # show a small window around mismatch
    context_radius = 20
    start = max(0, mismatch_pos - context_radius)
    end = min(min_len, mismatch_pos + context_radius)
    print("Context around mismatch (written vs reference):")
    print("W:", repr(ours[start:end]))
    print("R:", repr(ref[start:end]))
    return False


def main():
    decimal_places = prompt_decimal_places(default=10000)

    print(
        f"Computing sqrt(2) to {decimal_places} decimal places... (this may take a while)"
    )

    t0 = time.time()
    try:
        result_decimal = sqrt_2_high_precision(decimal_places)
    except Exception as e:
        print(f"Error computing sqrt(2): {e}")
        sys.exit(1)
    t1 = time.time()

    result_str = decimal_to_fixed_string(result_decimal, decimal_places)

    # Print brief summary (avoid printing extremely long output to console)
    print(f"Computation complete in {t1 - t0:.2f} seconds.")
    print(f"Integer part and first 80 chars: {result_str[:82]}")

    # Write to file
    write_result_to_file(result_str, RESULT_FILENAME)
    print(
        f"Result written to '{RESULT_FILENAME}' (UTF-8). File size: {os.path.getsize(RESULT_FILENAME)} bytes"
    )

    # Verify immediately
    print("Verifying the written result against a high-precision reference...")
    t2 = time.time()
    ok = verify_written_result(RESULT_FILENAME, decimal_places)
    t3 = time.time()
    print(f"Verification completed in {t3 - t2:.2f} seconds.")

    if ok:
        print("All good.")
    else:
        print("There was a mismatch. See details above.")

    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
