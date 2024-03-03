from aiocryptopay import AioCryptoPay
from aiocryptopay.models.invoice import Invoice
from aiocryptopay.utils import get_rate
from aiocryptopay.exceptions.factory import CodeErrorFactory


async def create_invoice(client: AioCryptoPay, amount: int, description: str, payload: dict, currency: str = "USDT"):
    rates = await client.get_exchange_rates()
    rate = get_rate(source='USDT', target="UAH", rates=rates)
    amount_in_crypto = amount / rate.rate
    try:
        invoice: Invoice = await client.create_invoice(
            amount=amount_in_crypto,
            asset=currency,
            description=description,
            payload=payload,
            expires_in=3000

        )
        return invoice
    except CodeErrorFactory as e:
        return False


async def check_signature(client: AioCryptoPay, body_text, crypto_pay_signature):
    return client.check_signature(body_text=body_text, crypto_pay_signature=crypto_pay_signature)
