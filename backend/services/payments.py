import base64
import json
from json import JSONDecodeError

from binascii import Error
from starlette.requests import Request

from models import Driver
from routers import AnonymousRouter
from views.payments import PaymentToken


async def parse_payment_token(token: str) -> PaymentToken:
    from exceptions import NotFound

    try:
        token = base64.b64decode(token.encode(), altchars=None, validate=False)
        data = json.loads(token.decode())
    except (Error, UnicodeDecodeError, JSONDecodeError):
        raise NotFound
    return PaymentToken(**data)


async def generate_payment_link(
        request: Request,
        router: AnonymousRouter,
        driver: Driver,
        total_cost: float,
        month: int,
        year: int
) -> str:
    data = PaymentToken(
        garage_id=driver.garage.id,
        driver_id=driver.id,
        email=driver.email,
        total_cost=total_cost * 100,
        month=month,
        year=year
    )
    token = base64.b64encode(json.dumps(data.dict()).encode()).decode()
    url = router.url_path_for("perform_prepayment", token=token)
    link = f"{request.base_url.scheme}://{request.base_url.hostname}{url}"
    return link
