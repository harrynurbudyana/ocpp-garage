from pydantic import BaseModel


class PaymentToken(BaseModel):
    garage_id: str
    driver_id: str
    email: str
    total_cost: int  # in cents
    year: int
    month: int


class PaymentSession(BaseModel):
    url: str
