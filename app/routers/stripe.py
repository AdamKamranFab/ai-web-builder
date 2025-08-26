import os
from fastapi import APIRouter, Depends, HTTPException
from app.models.stripe import StripeModel, StripePriceModel, StripeCheckoutSessionModel

stripe_router = APIRouter(prefix="/stripe", tags=["Stripe"])


@stripe_router.post('/create-product')
async def create_product(
        payload: StripeModel
):
    try:
        product = payload.create_product()

        return {
            "product_id": product.get('id')
        }
    except BaseException as e:
        raise e


@stripe_router.post('/create-price')
async def create_price(
        payload: StripePriceModel
):
    try:
        price = payload.create_price()
        return {"price_id": price["id"]}

    except BaseException as e:
        raise e


@stripe_router.post('/create-session')
async def create_session(
        payload: StripeCheckoutSessionModel
):
    try:
        session = payload.create_checkout_session()
        return {"checkout_url": session.url}

    except BaseException as e:
        raise e
