from pydantic import BaseModel


class PaymentToken(BaseModel):
    amount: int  # in cents
    charge_point_id: str
    connector_id: int
    track_id: str | None = None


class CheckoutSession(BaseModel):
    url: str
