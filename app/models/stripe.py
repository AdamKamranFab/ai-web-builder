import stripe
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class StripeModel(BaseModel):
    name: str
    description: Optional[str] = None

    def create_product(self):
        product = stripe.Product.create(
            name=self.name,
            description=self.description
        )
        return product


class StripePriceModel(BaseModel):
    product_id: str
    unit_amount: str
    interval: Optional[str] = None
    currency: Optional[str] = None

    def create_price(self):
        price = stripe.Price.create(
            product=self.product_id,
            unit_amount=self.unit_amount,
            currency=self.currency,
            recurring={"interval": self.interval}
        )
        return price


class StripeCheckoutSessionModel(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str

    def create_checkout_session(self):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": self.price_id,
                "quantity": 1
            }],
            mode="subscription",
            success_url=self.success_url,
            cancel_url=self.cancel_url,
        )
        return session
