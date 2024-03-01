import hashlib
import hmac
import json

from aiocryptopay import AioCryptoPay
from aiocryptopay.models.invoice import Invoice


async def create_invoice(client: AioCryptoPay, amount: int, description: str, payload: dict, currency: str = "USDT"):
    invoice: Invoice = await client.create_invoice(
        amount=1,  # TODO: CHANGE TO amount
        asset=currency,
        description=description,
        payload=payload,
        expires_in=3000

    )
    return invoice


async def check_signature(client: AioCryptoPay, body_text, crypto_pay_signature):
    return client.check_signature(body_text=body_text, crypto_pay_signature=crypto_pay_signature)
