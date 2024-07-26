from datetime import date
from pydantic import BaseModel

class SettlementRequest(BaseModel):
    merchant_id: str
    settlement_date: date

