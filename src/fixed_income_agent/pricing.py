from __future__ import annotations

from datetime import date

from .analytics import bond_price_vs_yield, plot_bond_price_vs_yield


def year_fraction(d1: date, d2: date) -> float:
    """Return the time to maturity as a year fraction.

    This is a simplified approximation using a 365-day year.
    """
    return (d2 - d1).days / 365.0


def price_bond(bond, curve, valuation_date: date) -> float:
    """Price a bond by discounting its future cash flows.

    In this simplified version, we assume:
    - the bond pays one coupon at maturity
    - the discount curve is flat
    - we approximate the time remaining as a simple year fraction

    Price is:
        PV(face) + PV(coupon)
    """
    if valuation_date > bond.maturity:
        raise ValueError("Valuation date cannot be after bond maturity.")

    # Time remaining from the valuation date to the maturity date.
    t = year_fraction(valuation_date, bond.maturity)

    # Present value of principal repayment at maturity.
    pv_face = bond.face * curve.discount(t)

    # Present value of annual coupon payment at maturity.
    pv_coupon = bond.annual_coupon() * curve.discount(t)

    # Total bond price.
    return pv_face + pv_coupon


__all__ = [
    "year_fraction",
    "price_bond",
    "bond_price_vs_yield",
    "plot_bond_price_vs_yield",
]
