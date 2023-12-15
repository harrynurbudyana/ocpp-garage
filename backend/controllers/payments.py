from traceback import format_exc

from async_stripe import stripe
from fastapi import Request, Depends
from loguru import logger
from pyocpp_contrib.decorators import message_id_generator
from starlette import status

from core import settings
from core.database import get_contextual_session
from core.fields import Currency
from core.utils import generate_host_url
from permissions.charge_points import use_data_if_allowed
from routers import AnonymousRouter
from services.charge_points import get_charge_point_or_404
from services.ocpp.remote_start_transaction import process_remote_start_transaction_call
from services.transactions import memorize_session_context, cost_to_watts
from views.payments import CheckoutSession, PaymentContext

public_router = AnonymousRouter()
stripe.api_key = settings.STRIPE_API_KEY


@public_router.post(
    "/stripe-webhook",
    status_code=status.HTTP_200_OK
)
async def confirm_payment(payload: dict):
    try:
        event = stripe.Event.construct_from(payload, stripe.api_key)
    except Exception:
        logger.error(f"Could not parse event from stripe %r" % format_exc())
        return

    logger.info(f"Got request from the stripe (type={event.type}, metadata={event.data.object})")

    if event.type == 'checkout.session.completed':
        metadata = event.data.object.metadata
        logger.info(f"Process successful payment (context={metadata})")
        context = PaymentContext(**metadata)

        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, context.charge_point_id)
            watts_limit = await cost_to_watts(charge_point.garage.daily_rate, context.amount)
            await memorize_session_context(context.charge_point_id, context.connector_id, context.track_id)

            logger.info(f"RemoteStartTransaction -> | Start process call request (context={context})")

            await process_remote_start_transaction_call(
                session,
                watts_limit,
                charge_point_id=context.charge_point_id,
                connector_id=context.connector_id,
                id_tag=charge_point.id,
                message_id=message_id_generator()
            )
            await session.commit()

        logger.info(f"Successful payment (context={context})")


@public_router.post(
    "/payments/checkout",
    status_code=status.HTTP_200_OK,
    response_model=CheckoutSession
)
async def create_checkout_session(
        request: Request,
        data=Depends(use_data_if_allowed)
):
    logger.info(f"Start create a payment checkout (data={data})")
    checkout_session = await stripe.checkout.Session.create(
        line_items=[
            {
                "quantity": 1,
                "price_data": {
                    "currency": Currency.usd.value,
                    "unit_amount": data.amount,
                    "product_data": {
                        "name": f"EV charging service."
                    }
                }
            },
        ],
        metadata=data.dict(),
        mode='payment',
        success_url=generate_host_url(request) + f'/transactions/{data.track_id}'
    )
    logger.info(f"Created a payment checkout (data={data.dict()})")
    return CheckoutSession(url=checkout_session.url)
