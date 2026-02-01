from datetime import datetime
from enum import Enum
from typing import Optional
from odmantic import Field, Model, ObjectId


class PaymentMethod(str, Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    UPI = "UPI"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"


class TransactionStatus(str, Enum):
    INITIATED = "INITIATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class Transaction(Model):
    """
    Model representing a payment transaction for a booking.
    """

    booking_id: ObjectId = Field(..., description="The booking this payment belongs to")
    user_id: ObjectId = Field(..., description="User who made the payment")

    amount: float = Field(..., description="Amount paid")
    currency: str = Field(default="INR")

    payment_method: Optional[PaymentMethod] = Field(default=None)
    status: TransactionStatus = Field(default=TransactionStatus.INITIATED)

    # External reference (e.g. Razorpay/Stripe ID)
    gateway_transaction_id: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"collection": "transactions"}
