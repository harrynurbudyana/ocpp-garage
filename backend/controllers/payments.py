from traceback import format_exc

from async_stripe import stripe
from fastapi import Request
from loguru import logger
from starlette import status

from core import settings
from core.database import get_contextual_session
from exceptions import NotFound
from routers import AnonymousRouter
from services.drivers import get_driver, find_driver
from services.payments import parse_payment_token
from views.payments import PaymentToken, PaymentSession

payments_router = AnonymousRouter()
stripe.api_key = settings.STRIPE_API_KEY


@payments_router.post(
    "/stripe-webhook",
    status_code=status.HTTP_200_OK
)
async def confirm_payment(payload: dict):
    try:
        event = stripe.Event.construct_from(payload, stripe.api_key)
    except Exception:
        logger.error(f"Could not parse event from stripe %r" % format_exc())
        return

    if event.type == 'checkout.session.completed':
        await stripe.PaymentIntent.modify(
            event.data.object.payment_intent,
            metadata=event.data.object.metadata
        )
    if event.type == 'payment_intent.succeeded':
        async with get_contextual_session() as session:
            driver = await find_driver(session, event.data.object.customer)
        if driver:
            logger.info(
                f"Successful payment from driver={driver.id}, customer={driver.customer_id}, amount={event.data.object.amount}")


@payments_router.post(
    "/payments/session",
    status_code=status.HTTP_200_OK,
    response_model=PaymentSession
)
async def create_payment_session(request: Request, data: PaymentToken):
    async with get_contextual_session() as session:
        driver = await get_driver(session, data.garage_id, data.driver_id)

    link = f"{request.base_url.scheme}://{request.base_url.hostname}"
    checkout_session = await stripe.checkout.Session.create(
        line_items=[
            {
                "quantity": 1,
                "price_data": {
                    "currency": "nok",
                    "unit_amount": data.total_cost,
                    "product_data": {
                        "name": f"Electricity compensation for {data.year} {data.month}"
                    }
                }
            },
        ],
        customer=driver.customer_id,
        metadata=data.dict(),
        mode='payment',
        success_url=link + f'/payments/success'
    )
    return PaymentSession(url=checkout_session.url)


@payments_router.get(
    "/payments/{token}",
    status_code=status.HTTP_200_OK,
    response_model=PaymentToken
)
async def perform_prepayment(token: str):
    """
    Check if bill is not covered and clarify payment details
    """
    payment_data = await parse_payment_token(token)
    async with get_contextual_session() as session:
        driver = await get_driver(session, payment_data.garage_id, payment_data.driver_id)

    intents = await stripe.PaymentIntent.list(customer=driver.customer_id, limit=10)

    # To don't allow double payment
    async for intent in intents.auto_paging_iter():
        obj = stripe.PaymentIntent.construct_from(intent, stripe.api_key)
        metadata = PaymentToken(**obj.metadata)
        if all([
            obj.status == "succeeded",
            payment_data.garage_id == metadata.garage_id,
            payment_data.year == metadata.year,
            payment_data.month == metadata.month
        ]):
            raise NotFound

    return payment_data
