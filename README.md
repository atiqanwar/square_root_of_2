# Square Root of 2 Calculator

This project calculates the square root of 2 to 10,000 decimal places using Python's `decimal` module for high-precision arithmetic.

## Files

- `sqrt_2.py` - Main script that calculates √2 to 10,000 decimal places
- `sqrt_2_result.txt` - Output file containing the result
- `README.md` - This file

## How It Works

The calculation uses Newton's method (also known as the Babylonian method) to compute the square root:

```
x_{n+1} = (x_n + 2/x_n) / 2
```

Starting with an initial guess of 1.5, the algorithm iteratively refines the approximation until the desired precision is achieved.

## Requirements

- Python 3.x

## Usage

Run the script directly:

```bash
python sqrt_2.py
```

The result will be:
1. Displayed on the console
2. Saved to `sqrt_2_result.txt`

## Precision

The script calculates √2 to exactly 10,000 decimal places. The result has been verified to match known high-precision values of the square root of 2.

## Sample Output

The first few digits of the result are:
1.41421356237309504880168872420969807856967187537694...

## Implementation Details

- Uses Python's `decimal` module for arbitrary precision arithmetic
- Sets precision higher than needed during calculation to avoid rounding errors
- Implements Newton's method for rapid convergence
- Formats output for readability

```
