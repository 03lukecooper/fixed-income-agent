# Fixed Income Agent

This project is a small fixed-income analytics starter. It shows how to model a bond, price it using a discount curve, value a small bond portfolio, and run a very simple curve-shock scenario.

## What the project does

- Defines a simple bond object with coupon, maturity, and face value
- Prices bonds using discount factors from a yield curve
- Values a portfolio of bonds by quantity
- Simulates small shifts in the curve to see how NAV changes
- Plots a bond price-vs-yield curve and saves it as a PNG

## Quick start

```bash
python -m pip install -e .
python main.py
python -m pytest -q
```

## Main files

- `src/fixed_income_agent/instruments.py` defines the bond and portfolio objects
- `src/fixed_income_agent/yield_curve.py` defines the discount curve
- `src/fixed_income_agent/pricing.py` prices bonds and exposes analytic helpers
- `src/fixed_income_agent/analytics.py` plots bond price vs yield
- `main.py` is the example script that runs the workflow
- `tests/test_agent.py` validates the key behaviors

## Simple summary

The code is intentionally small and educational: it is not a full trading system, but it is a good base for building one.
