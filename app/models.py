from datetime import date
from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from dataclasses import dataclass
from enum import Enum

class SettlementRequest(BaseModel):
    merchant_id: str
    settlement_date: date

class SettlementResponse(BaseModel):
    merchant_id: str
    settlement_date: date
    settlement_amount: Decimal
    transaction_count: int

class TransactionType(Enum):
    PURCHASE = "PURCHASE"
    REFUND = "REFUND"
    SALE = "SALE"

@dataclass
class Transaction:
    id: str
    created_at: datetime
    updated_at: datetime
    amount: Decimal
    type: TransactionType
    customer: str
    merchant: str
    order: str
