from pydantic import BaseModel


class SimpleGridProviderView(BaseModel):
    id: str
    name: str
    postnummer: str

    class Config:
        orm_mode = True


class GridProviderView(BaseModel):
    name: str
    region: str
    postnummer: str
    daily_rate: float
    nightly_rate: float

    class Config:
        orm_mode = True