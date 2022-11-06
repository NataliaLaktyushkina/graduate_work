from fastapi import APIRouter, Depends
from models.payment import PaymentAccepted, Payment
from models.payment import SubscriptionId, PaymentStatus, PaymentType
from services.jwt_check import JWTBearer
from services.payments import PaymentHandler, get_payment_handler
from core.config import settings

router = APIRouter()


@router.post('/', description='Pay for subscription',
             response_model=PaymentAccepted,
             response_description='Payment sent')
async def proceed_payment(
        payment_type: PaymentType,
        subscription_type: SubscriptionId,
        user_id: str = Depends(JWTBearer()),
        service: PaymentHandler = Depends(get_payment_handler),
) -> PaymentAccepted:
    payment = Payment(payment_id=subscription_type,
                      topic=settings.TOPIC_PAYMENT,
                      status=PaymentStatus.new,
                      payment_type=payment_type)
    return await service.send_payment(payment, user_id)
