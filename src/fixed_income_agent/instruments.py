from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Sequence


@dataclass
class Bond:
    """A simple fixed-rate bond model.

    In real life, a bond has a coupon, maturity, face value, and sometimes an
    issue date. Here, we keep it small and focused on pricing logic.
    """

    isin: str
    maturity: date
    coupon: float
    face: float
    frequency: int = 1
    issue_date: Optional[date] = None

    def annual_coupon(self) -> float:
        """Annual coupon cash flow for the bond.

        Example: a 5% coupon on a 100 face bond pays 5 per year.
        """
        return self.face * self.coupon

    def cash_flows(self) -> list[float]:
        """Return a simple list of cash-flow values.

        This is intentionally basic; in a fuller system, each coupon would have a
        distinct date and cash-flow schedule.
        """
        return [self.annual_coupon() for _ in range(self.frequency)]


@dataclass
class BondPortfolio:
    """A basic portfolio of bonds and quantities.

    Each position is a tuple of (Bond, quantity). This lets us value a basket of
    bonds under a given curve.
    """

    positions: list[tuple[Bond, float]] = field(default_factory=list)

    def add_position(self, bond: Bond, quantity: float) -> None:
        """Add a bond holding to the portfolio."""
        if quantity == 0:
            raise ValueError("Quantity cannot be zero.")
        self.positions.append((bond, quantity))

    def market_value(self, curve, valuation_date) -> float:
        """Compute total market value of the portfolio at a valuation date.

        We price each bond under the same curve and multiply by the number of
        units held.
        """
        from .pricing import price_bond

        return sum(
            quantity * price_bond(bond, curve, valuation_date)
            for bond, quantity in self.positions
        )

    def nav(self, curve, valuation_date) -> float:
        """NAV is the same as market value for this simplified portfolio."""
        return self.market_value(curve, valuation_date)

    def simulate_curve_shocks(self, shocks: Sequence[float], valuation_date, *, base_rate: float = 0.04):
        """Apply a set of parallel curve shifts and measure the portfolio NAV.

        Example: [0.00, 0.01, 0.02] means a 0%, 100 bps, and 200 bps shift in the
        yield curve. This is a simple stress-test pattern.
        """
        from .yield_curve import FlatCurve

        return {
            shock: self.nav(FlatCurve(base_rate + shock), valuation_date)
            for shock in shocks
        }
