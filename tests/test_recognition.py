from datetime import date
from effora.engine import recognize, Contract


def _contract(**kwargs):
    defaults = dict(
        contract_id="ctr_test",
        customer_id="cust_test",
        currency="USD",
        total_value=12000,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
        performance_obligations=[
            {"name": "SaaS Access", "value": 12000, "recognition_method": "ratable"}
        ]
    )
    defaults.update(kwargs)
    return Contract(**defaults)


def test_total_recognized_equals_contract_value():
    """Sum of all recognized amounts must equal total contract value."""
    s = recognize(_contract())
    total = sum(e.recognized for e in s.schedule)
    assert round(total, 2) == 12000.00


def test_final_deferred_is_zero():
    """Deferred balance must reach zero at end of contract."""
    s = recognize(_contract())
    assert s.schedule[-1].deferred == 0.00


def test_partial_month_start():
    """Contract starting mid-month should recognize less in first month."""
    s = recognize(_contract(start_date=date(2026, 1, 15)))
    first = s.schedule[0].recognized
    full_month = s.schedule[1].recognized  # February — full month
    assert first < full_month


def test_twelve_periods_full_year():
    """Full year contract should produce exactly 12 monthly periods."""
    s = recognize(_contract())
    assert len(s.schedule) == 12


def test_on_completion_recognized_in_first_month():
    """on_completion obligation must be fully recognized in start month."""
    s = recognize(_contract(
        total_value=3000,
        performance_obligations=[
            {"name": "Onboarding", "value": 3000, "recognition_method": "on_completion"}
        ]
    ))
    assert s.schedule[0].recognized == 3000.00
    assert s.schedule[0].deferred == 0.00