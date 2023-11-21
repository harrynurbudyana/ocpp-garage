from pydantic import BaseModel


class PaymentReminderView(BaseModel):
    month: int
    year: int
    total_cost: float
    total_kw: float