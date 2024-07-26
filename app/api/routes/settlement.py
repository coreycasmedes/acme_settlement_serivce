from fastapi import APIRouter, Query, HTTPException
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from app.models import Transaction, TransactionType, SettlementResponse
from app.core.config import settings
from decimal import Decimal
import logging
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class CustomAcmeServiceException(Exception):
    """
    Custom exception for when ACME service is readily unresponsive 
    """
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


@router.get("/settlement", response_model=SettlementResponse)
def get_settlements(
    merchant_id: str = Query(..., description="The ID of the merchant"),
    settlement_date: date = Query(..., description="The date for the settlement")
) -> SettlementResponse:
    """
    Calculate and return the settlement balance for a given merchant and date
    """
    # TODO Convert merchant string to uuid if they dont give merchant as uuid
    try:
        transactions = get_merchant_transactions(merchant_id, settlement_date)
        settlement_amount = calculate_settlement_amount(transactions)

        return SettlementResponse(
            merchant_id=merchant_id,
            settlement_date=settlement_date,
            settlement_amount=settlement_amount,
            transaction_count=len(transactions)
        )
    except CustomAcmeServiceException:
        logger.error(f"Max retries exceeded for merchant {merchant_id}")
        raise HTTPException(status_code=503, detail="Unable to fetch complete transaction data after multiple attempts")
    except Exception as e:
        logger.exception(f"Unexpected error in get_settlements for merchant {merchant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


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


def get_merchant_transactions(merchant_id: str, settlement_date: date) -> list[Transaction]:
    """
    Fetches all the transactions for a given merchant and settlement_date
    """
    merchant_transactions = []
    next_url = f"{settings.API_BASE_URL}/transactions"

    # Typically I would use a built in library like tenacity to handle retries, but due to time constraints im doing it myself
    attempt = 0
    max_number_of_retries = 8
    time_between_retries = 1

    while next_url and attempt < max_number_of_retries:
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
        except requests.HTTPError as exception:
            if exception.response.status_code == 409:
                logger.warning(f"Conflict experienced when querying for merchant {merchant_id} transactions")
            elif exception.response.status_code == 413:
                logger.warning(f"Request too large for merchant {merchant_id}. Attempting to reduce time slice.")
            elif exception.response.status_code == 425:
                logger.warning(f"")
            else:
                logger.error(f"HTTP error occurred: {exception}")
        except requests.RequestException as exception:
            logger.error(f"Error fetching transactions for merchant {merchant_id}: {str(exception)}")
        except ValueError as exception:
            logger.error(f"Error parsing transaction data for merchant {merchant_id}: {str(exception)}")
        except Exception as exception:
            logger.exception(f"Unexpected error fetching transactions for merchant {merchant_id}: {str(exception)}")
        finally:
            attempt += 1
            if attempt < max_number_of_retries and next_url is not None:
                time.sleep(time_between_retries)
    
    if attempt == max_number_of_retries:
        raise CustomAcmeServiceException("Maximum numbers of API call attempts made,"
            + "gracefully failing to avoid rate limiting issues")
        
    return merchant_transactions
