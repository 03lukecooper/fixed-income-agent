from __future__ import annotations


class FlatCurve:
    """A very simple curve that assumes the same interest rate at every maturity.

    This is not a realistic multi-curve model, but it is useful for learning the
    core bond-pricing concept: discount cash flows using a rate.
    """

    def __init__(self, rate: float):
        # The curve is defined by a single flat rate, for example 4%.
        self.rate = rate

    def discount(self, t: float) -> float:
        """Return the discount factor for time t.

        A discount factor is the present value of $1 received at time t.
        Formula: DF(t) = 1 / (1 + r)^t
        """
        return 1.0 / (1.0 + self.rate) ** t

    def forward_rate(self, t: float) -> float:
        """Return a simple forward rate placeholder.

        For a flat curve, the forward rate is the same as the current rate.
        """
        return self.rate
