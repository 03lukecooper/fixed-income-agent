from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .yield_curve import FlatCurve


def bond_price_vs_yield(bond, yields: Sequence[float], valuation_date, *, freq: int = 1):
    """Return a list of (yield, price) tuples for a bond across a range of yields.

    This is a quick sensitivity analysis: if the market yield changes, how does
    the bond price change? In general, bond prices fall when yields rise.
    """
    results = []
    for y in yields:
        # Treat the market as a flat curve at the current yield level.
        curve = FlatCurve(y)

        # Coupon is divided by the number of payment periods if needed.
        coupon = bond.annual_coupon() / freq
        t = (bond.maturity - valuation_date).days / 365.0

        pv_coupon = 0.0
        for i in range(1, freq + 1):
            # For a simple example, spread the cash flows across the remaining time.
            cash_flow_time = t * (i / freq)
            pv_coupon += coupon * curve.discount(cash_flow_time)

        pv_face = bond.face * curve.discount(t)
        price = pv_coupon + pv_face
        results.append((y, price))
    return results


def plot_bond_price_vs_yield(bond, yields: Iterable[float], valuation_date, save_path=None, *, freq: int = 1):
    """Plot bond price against yield and optionally save the figure to disk."""
    yield_values = list(yields)
    prices = [price for _, price in bond_price_vs_yield(bond, yield_values, valuation_date, freq=freq)]

    # Create the figure and axes for the chart.
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot the relationship between yield and price.
    ax.plot(yield_values, prices, marker="o")
    ax.set_title(f"Bond price vs yield: {bond.isin}")
    ax.set_xlabel("Yield")
    ax.set_ylabel("Price")
    ax.grid(True, alpha=0.3)

    # Save the image to disk if a path was provided.
    if save_path is not None:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150)

    return fig, ax
