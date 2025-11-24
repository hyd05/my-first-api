import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def create_charge(payment_method_id: str, amount: float, currency: str = 'USD', description: str = 'LifeCoach AI Premium'):
    if not stripe.api_key:
        raise RuntimeError('STRIPE_SECRET_KEY not set')

    # Convert amount to cents (Stripe expects integers)
    amount_cents = int(amount * 100)

    try:
        # Create and confirm PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency.lower(),
            payment_method=payment_method_id,
            confirmation_method='automatic',
            description=description,
            confirm=True,
        )
        return intent.to_dict()
    except stripe.error.StripeError as e:
        raise RuntimeError(f"Stripe error: {e.user_message}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")