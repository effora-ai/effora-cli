from effora.engine.models import Contract
from effora.engine.recognition import recognize as _recognize
from effora.engine.models import RecognitionSchedule


def recognize(contract: dict) -> RecognitionSchedule:
    """
    Recognize revenue for a contract under ASC 606.

    Args:
        contract: dict matching the Effora canonical contract schema

    Returns:
        RecognitionSchedule with .schedule, .audit, .total_value

    Example:
        from effora.sdk import recognize

        schedule = recognize({
            "contract_id": "ctr_001",
            "customer_id": "cust_acme",
            "total_value": 12000,
            "currency": "USD",
            "start_date": "2026-01-01",
            "end_date": "2026-12-31",
            "performance_obligations": [
                {
                    "name": "Platform Access",
                    "value": 12000,
                    "recognition_method": "ratable"
                }
            ]
        })

        for entry in schedule.schedule:
            print(entry.period, entry.recognized)
    """
    c = Contract(**contract)
    return _recognize(c)