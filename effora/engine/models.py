from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import date


class PerformanceObligation(BaseModel):
    name: str
    value: float
    recognition_method: Literal["ratable", "on_completion"]


class Contract(BaseModel):
    contract_id: str
    customer_id: str
    currency: str = "USD"
    total_value: float
    start_date: date
    end_date: date
    performance_obligations: List[PerformanceObligation] = Field(min_length=1)


class MonthlyEntry(BaseModel):
    period: str          # "2026-01"
    recognized: float
    deferred: float


class RecognitionSchedule(BaseModel):
    contract_id: str
    customer_id: str
    currency: str
    total_value: float
    schedule: List[MonthlyEntry]
    audit: dict