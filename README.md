# Square Root of 2 Calculator

This project computes the square root of 2 to a user-specified number of decimal places using Python's `decimal` module for high-precision arithmetic, and verifies the written result immediately after creation.

## Project files

- `sqrt_2.py` - Main interactive script:
  - Prompts for the number of decimal places (default 10,000).
  - Computes √2 using Newton's method with high internal precision.
  - Truncates (no rounding up) to exactly the requested number of fractional digits.
  - Writes the fixed-length result to `sqrt_2_result.txt` (UTF-8).
  - Verifies the written file against a high-precision Decimal reference and reports success or the first mismatch.
- `verify_sqrt2.py` - (older/alternate) verification helper script (may be present).
- `sqrt_2_result.txt` - Output file produced by `sqrt_2.py`. This file contains the computed value as a fixed-point decimal string (e.g. "1.4142...").

## How it works

The computation uses Newton's (Babylonian) method:

```
x_{n+1} = (x_n + 2 / x_n) / 2
```

Starting from an initial guess (1.5), the iteration rapidly converges. The script:

- Uses an extra precision margin during iteration to avoid rounding errors.
- Stops when the change between iterations is smaller than a convergence threshold tied to the requested digits.
- Truncates the final Decimal to exactly N fractional digits using ROUND_DOWN (so the output contains exactly N digits after the decimal point).
- Writes the result to disk and then computes a reference sqrt(2) with extra precision and compares the two strings to ensure they match for all requested digits.

## Requirements

- Python 3.8+ (recommended)
- No external libraries required; uses Python's stdlib `decimal` module

## Usage

Interactive (recommended):

```bash
python sqrt_2.py
```

- You will be prompted for the number of decimal places. Press Enter to accept the default (10000).
- For very large requests (hundreds of thousands of digits), the script will ask for confirmation because the computation can be slow and memory-intensive.

Example session:
- Enter number of decimal places (non-negative integer, default 10000): 10000
- Script will compute, write `sqrt_2_result.txt`, then verify the written result and report success or the first mismatch.

Non-interactive / automation:
- The current script is interactive. If you need non-interactive operation (flags like `--digits` and `--output`), consider adding argparse support (this can be added on request).

## Output

- The output file `sqrt_2_result.txt` contains a single fixed-point decimal string:
  - Example prefix: `1.41421356...`
  - The file is written in UTF-8 and contains exactly one leading `1`, one decimal point `.`, and exactly N fractional digits (for N requested digits).

## Verification

- After writing the result, the script computes a high-precision reference using `Decimal(2).sqrt()` and truncates it to the requested number of digits using the same truncation policy.
- The script then compares the written file and the reference string exactly. If they differ, it reports the first mismatch index and shows context for debugging.

## Performance notes and caveats

- Memory and CPU usage grow with the requested number of digits. Very large requests (hundreds of thousands of digits or more) may be slow or run out of memory on smaller machines.
- The script intentionally truncates (ROUND_DOWN) to produce a deterministic, exact-length output. If you prefer rounding instead of truncation, the code can be adjusted.
- For automated or repeated large computations, consider running on a machine with sufficient RAM and CPU and/or adding progress reporting and checkpoints.

## Contributing / Extensions

Possible improvements you can request:
- Add argparse flags for non-interactive use (`--digits`, `--output`, `--verify`).
- Add progress logging or a resumable checkpoint mechanism for extremely large computations.
- Provide an option to choose rounding mode (ROUND_HALF_EVEN vs ROUND_DOWN).
- Provide a unit-test script that asserts correctness for several small N (e.g., 0, 1, 10, 100).

## Example first digits

The first few digits are (for reference):
```
1.41421356237309504880168872420969807856967187537694...
```

