from pydantic import BaseModel


class SimpleGridProviderView(BaseModel):
    id: str
    name: str
    postnummer: str

    class Config:
        orm_mode = True
