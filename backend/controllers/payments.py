from traceback import format_exc
from uuid import uuid4

from async_stripe import stripe
from fastapi import Request
from loguru import logger
from ocpp.v16.enums import ChargePointStatus
from pyocpp_contrib.decorators import message_id_generator
from starlette import status

from core import settings
from core.database import get_contextual_session
from exceptions import Forbidden
from routers import AnonymousRouter
from services.charge_points import get_charge_point_or_404, get_connector_or_404
from services.ocpp.remote_start_transaction import process_remote_start_transaction_call
from services.transactions import memorize_track_id
from views.payments import CheckoutSession, PaymentToken

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

    logger.info(f"Got request from the stripe (type={event.type}, metadata={event.data.object.metadata})")

    if event.type == 'checkout.session.completed':
        await stripe.PaymentIntent.modify(
            event.data.object.payment_intent,
            metadata=event.data.object.metadata
        )

    if event.type == 'payment_intent.succeeded':
        intent = await stripe.PaymentIntent.retrieve(event.data.object.id)
        logger.info(f"Process successful payment (context={intent.metadata})")
        # this event type might be duplicated
        # verify wrong duplicate with empty metadata
        if not intent.metadata:
            return
        context = PaymentToken(**intent.metadata)

        async with get_contextual_session() as session:
            charge_point = await get_charge_point_or_404(session, context.charge_point_id)
            rate = charge_point.garage.daily_rate
            # an amount is used in cents
            # lets convert it into dollars
            amount = event.data.object.amount / 100
            watts_limit = (amount / float(rate)) * 1000

            await memorize_track_id(context.charge_point_id, context.connector_id, context.track_id)

            logger.info(f"RemoteStartTransaction -> | Start process call request (context={context})")
            async with get_contextual_session() as session:
                await process_remote_start_transaction_call(
                    session,
                    watts_limit,
                    charge_point_id=context.charge_point_id,
                    connector_id=context.connector_id,
                    id_tag=charge_point.id,
                    message_id=message_id_generator()
                )
                await session.commit()

        logger.info(
            f"Successful payment (context={context}, amount={event.data.object.amount})")


@public_router.post(
    "/payments/checkout",
    status_code=status.HTTP_200_OK,
    response_model=CheckoutSession
)
async def create_checkout_session(request: Request, data: PaymentToken):
    data.track_id = str(uuid4())

    async with get_contextual_session() as session:
        connector = await get_connector_or_404(session, data.charge_point_id, data.connector_id)
        if ChargePointStatus(connector.status) is not ChargePointStatus.available:
            raise Forbidden(detail="Connector is already taken.")

    logger.info(f"Start create a payment checkout (data={data})")
    link = f"{request.base_url.scheme}://{request.base_url.hostname}"
    checkout_session = await stripe.checkout.Session.create(
        line_items=[
            {
                "quantity": 1,
                "price_data": {
                    "currency": "usd",
                    "unit_amount": data.amount,
                    "product_data": {
                        "name": f"EV charging service."
                    }
                }
            },
        ],
        metadata=data.dict(),
        mode='payment',
        success_url=link + f'/transactions/{data.track_id}'
    )
    logger.info(f"Created a payment checkout (data={data.dict()})")
    return CheckoutSession(url=checkout_session.url)
