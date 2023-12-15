from uuid import uuid4

from pydantic import BaseModel, Field


class PaymentContext(BaseModel):
    amount: int  # in cents
    charge_point_id: str
    connector_id: int
    track_id: str = Field(default_factory=lambda: uuid4().hex)


class CheckoutSession(BaseModel):
    url: str
