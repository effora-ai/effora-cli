from datetime import date, timedelta
from collections import defaultdict
from .models import Contract, MonthlyEntry, RecognitionSchedule


def _date_range(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def _recognize_ratable(value: float, start: date, end: date) -> dict:
    """Spread value evenly across every day in [start, end]."""
    days = list(_date_range(start, end))
    total_days = len(days)
    daily_rate = value / total_days
    by_month = defaultdict(float)
    for d in days:
        key = f"{d.year}-{d.month:02d}"
        by_month[key] += daily_rate
    return dict(by_month)


def _recognize_on_completion(value: float, start: date) -> dict:
    """Recognize full value in the month of start date."""
    key = f"{start.year}-{start.month:02d}"
    return {key: value}


def recognize(contract: Contract) -> RecognitionSchedule:
    combined: dict = defaultdict(float)

    for ob in contract.performance_obligations:
        if ob.recognition_method == "ratable":
            monthly = _recognize_ratable(ob.value, contract.start_date, contract.end_date)
        elif ob.recognition_method == "on_completion":
            monthly = _recognize_on_completion(ob.value, contract.start_date)

        for period, amount in monthly.items():
            combined[period] += amount

    # build schedule with running deferred balance
    # last period absorbs any rounding remainder
    schedule = []
    cumulative = 0.0
    sorted_periods = sorted(combined.keys())
    for i, period in enumerate(sorted_periods):
        is_last = i == len(sorted_periods) - 1
        if is_last:
            recognized = round(contract.total_value - cumulative, 2)
        else:
            recognized = round(combined[period], 2)
        cumulative += recognized
        deferred = round(contract.total_value - cumulative, 2)
        schedule.append(MonthlyEntry(
            period=period,
            recognized=recognized,
            deferred=max(deferred, 0.0)
        ))

    return RecognitionSchedule(
        contract_id=contract.contract_id,
        customer_id=contract.customer_id,
        currency=contract.currency,
        total_value=contract.total_value,
        schedule=schedule,
        audit={
            "standard": "ASC 606",
            "engine_version": "0.1.0",
            "recognized_total": round(sum(e.recognized for e in schedule), 2),
            "generated_at": date.today().isoformat(),
        }
    )