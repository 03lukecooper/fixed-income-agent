from datetime import date

from fixed_income_agent.agent import SimpleAgent, Tool
from fixed_income_agent.instruments import Bond, BondPortfolio
from fixed_income_agent.pricing import bond_price_vs_yield, plot_bond_price_vs_yield
from fixed_income_agent.yield_curve import FlatCurve


def test_tool_registration_and_execution():
    agent = SimpleAgent()

    def greeting(name: str) -> str:
        return f"Hello, {name}!"

    agent.register_tool("greet", greeting)

    result = agent.run("greet", "Ada")

    assert result == "Hello, Ada!"


def test_unknown_tool_raises_error():
    agent = SimpleAgent()

    try:
        agent.run("unknown_tool", "value")
    except ValueError as exc:
        assert "unknown_tool" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown tool")


def test_tool_object_is_valid():
    tool = Tool(name="echo", func=lambda x: x)
    assert tool.name == "echo"
    assert callable(tool.func)


def test_bond_price_vs_yield_monotonic():
    bond = Bond(isin="TEST123", maturity=date(2030, 1, 1), coupon=0.05, face=100)
    values = bond_price_vs_yield(bond, [0.02, 0.04], valuation_date=date(2025, 1, 1))

    assert len(values) == 2
    assert values[0][0] == 0.02
    assert values[1][0] == 0.04
    assert values[0][1] > values[1][1]


def test_plot_bond_price_vs_yield_creates_png(tmp_path):
    bond = Bond(isin="TEST123", maturity=date(2030, 1, 1), coupon=0.05, face=100)
    output = tmp_path / "bond_curve.png"

    fig, ax = plot_bond_price_vs_yield(
        bond,
        yields=[0.00, 0.02, 0.04],
        valuation_date=date(2025, 1, 1),
        save_path=output,
    )

    assert fig is not None
    assert ax is not None
    assert output.exists()


def test_bond_portfolio_nav_uses_quantity():
    bond = Bond(isin="TEST123", maturity=date(2030, 1, 1), coupon=0.05, face=100)
    portfolio = BondPortfolio()
    portfolio.add_position(bond, 2)

    nav = portfolio.nav(FlatCurve(0.04), date(2025, 1, 1))

    assert nav > 0
    assert nav == portfolio.market_value(FlatCurve(0.04), date(2025, 1, 1))


def test_curve_shock_simulation_changes_nav():
    bond = Bond(isin="TEST123", maturity=date(2030, 1, 1), coupon=0.05, face=100)
    portfolio = BondPortfolio()
    portfolio.add_position(bond, 1)

    base_nav = portfolio.nav(FlatCurve(0.04), date(2025, 1, 1))
    shocked = portfolio.simulate_curve_shocks([0.00, 0.01, 0.02], date(2025, 1, 1))

    assert base_nav > 0
    assert list(shocked.keys()) == [0.00, 0.01, 0.02]
    assert shocked[0.00] != shocked[0.02]
