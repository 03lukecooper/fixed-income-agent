from datetime import date
from pathlib import Path

from src.fixed_income_agent.instruments import Bond
from src.fixed_income_agent.yield_curve import FlatCurve
from src.fixed_income_agent.pricing import price_bond
from src.fixed_income_agent.analytics import plot_bond_price_vs_yield

# Create a yield curve
curve = FlatCurve(0.04)

# Create a bond
bond = Bond(
    isin="TEST123",
    maturity=date(2030, 1, 1),
    coupon=0.05,
    face=100,
)

# Price the bond
price = price_bond(bond, curve, date.today())
print("Bond price:", price)

# Save a simple bond price-vs-yield chart
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)
plot_bond_price_vs_yield(
    bond,
    yields=[0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
    valuation_date=date.today(),
    save_path=output_dir / "bond_price_vs_yield.png",
)
print(f"Saved bond chart to: {output_dir / 'bond_price_vs_yield.png'}")

