from fastapi import APIRouter, Query
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from app.models import Transaction, TransactionType, SettlementResponse
from decimal import Decimal
import logging
import requests

router = APIRouter()

@router.get("/settlement")
def get_settlements(
    merchant_id: str = Query(..., description="The ID of the merchant"),
    settlement_date: date = Query(..., description="The date for the settlement")
):
    """
    Calculate and return the settlement balance for a given merchant and date
    """
    # TODO Convert merchant string to uuid if they dont give merchant as uuid
    transactions = get_merchant_transactions(merchant_id, settlement_date)
    settlement_amount = calculate_settlement_amount(transactions)
    return settlement_amount

    print('raeched')

def calculate_settlement_amount(transactions: list[Transaction]) -> SettlementResponse:
    """
    Calculates the settlement amount given a list of transactions
    """
    settlement_amount = Decimal('0.00')
    for transaction in transactions:
        if transaction.type in (TransactionType.PURCHASE, TransactionType.SALE):
            settlement_amount += transaction.amount
        elif transaction.type == TransactionType.REFUND:
            settlement_amount -= transaction.amount
        else:
            raise ValueError("Unexpected transaction type" 
                + f"{transaction.type}, skipping to avoid erroneous calculations")
    return settlement_amount


def get_merchant_transactions(merchant_id: str, settlement_date: date):
    """
    Fetches all the transactions for a given merchant and settlement_date
    """
    merchant_transactions = []
    next_url = "https://api-engine-dev.clerq.io/tech_assessment/transactions" 
    while next_url:
        try:
            response = requests.get(
                next_url,
                params={
                    "merchant": merchant_id,
                    "created_at__gte": settlement_date.isoformat(),
                    "created_at__lt": (settlement_date + timedelta(days=1)).isoformat()
                }, 
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            merchant_transactions.extend([
                Transaction(
                    id=transaction['id'],
                    created_at=datetime.fromisoformat(transaction['created_at'].rstrip('Z')),
                    updated_at=datetime.fromisoformat(transaction['updated_at'].rstrip('Z')),
                    amount=Decimal(transaction['amount']),
                    type=TransactionType(transaction['type']),
                    customer=transaction['customer'],
                    merchant=transaction['merchant'],
                    order=transaction['order']
                ) for transaction in data['results']
            ])
            next_url = data['next']
        except Exception as e:
            continue
        
    return merchant_transactions

def get_settlement(merchant_id: str, settlement_date: date) -> dict:
    """
    Returns settlement amount for the merchant on a given date.
    """
    # iso_date = date.isoformat()
    # merchant_transactions = []
    # merchant_transactions = requests.get(
    #     'https://api-engine-dev.clerq.io/tech_assessment/transactions',
    #     params={
    #         "merchant": merchant_id,
    #         "created_at__gte": date.isoformat(),
    #         "created_at__lt": (date + timedelta(days=1)).isoformat()
    #     }, 
    #     timeout=5
    # )

    # Step 1 get all merchant transactions for date
    transactions = get_merchant_transactions(merchant_id, date)
    settlement_amount = calculate_settlement_amount(transactions) 
    return settlement_amount




answer = get_settlement("b0c9a871-f9b3-411e-b713-b5b17287f956", date(2023, 1, 13))
print(answer)
