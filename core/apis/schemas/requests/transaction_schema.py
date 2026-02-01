from pydantic import BaseModel, Field
from typing import Optional
from core.models.transaction_model import PaymentMethod, TransactionStatus


class TransactionCreate(BaseModel):
    booking_id: str = Field(..., description="Booking ID (hex string)")
    payment_method: PaymentMethod


class TransactionUpdate(BaseModel):
    status: TransactionStatus
    gateway_transaction_id: Optional[str] = None
