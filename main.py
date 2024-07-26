
# from dataclasses import dataclass
# from datetime import datetime, date, timedelta
# import logging
# import requests


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# BASE_URL = "https://api-engine-dev.clerq.io/tech_assessment"


# class AcmeClient:
#     def __init__(self, url) -> None:
#         self.url = url
#         self.headers = {"accept": "application/json"}
#         #self.

#     def get_customers():
#         return requests.get('https://api-engine-dev.clerq.io/tech_assessment/customers')
    
#     def get_customer(id: str):
#         return requests.get(f'https://api-engine-dev.clerq.io/tech_assessment/customers/{id}') 

#     def get_merchants():
#         return requests.get('https://api-engine-dev.clerq.io/tech_assessment/merchants')
    
#     def get_merchant(id: str):
#         return requests.get(f'https://api-engine-dev.clerq.io/tech_assessment/merchants/{id}') 

#     def get_orders():
#         return requests.get('https://api-engine-dev.clerq.io/tech_assessment/orders')
    
#     def get_order(id: str):
#         return requests.get(f'https://api-engine-dev.clerq.io/tech_assessment/orders/{id}')


# #curl -X 'GET' \
# #   'https://api-engine-dev.clerq.io/tech_assessment/customers/' \
# #   -H 'accept: application/json'
# #requests.get('https://api-engine-dev.clerq.io/tech_assessment/customers/')


# # Notes 
# # get merchant by id seems to be throwing a mix of 409 and 200s
# # get txns throws 510 and 200s


# # Customer
# customer = {
#     'id': 'dcf2c5c0-3ecd-41ef-b757-8a7f6ef56ec4', 
#     'created_at': '2022-12-13T07:58:58Z', 
#     'updated_at': '2022-12-13T07:58:58Z', 
#     'first_name': 'Christopher', 'last_name': 'Anderson', 
#     'phone': '(641)205-4767', 
#     'address': 'Unit 3164 Box 9327\nDPO AA 34333', 
#     'email': 'benjaminmoody@example.org'
# }

# # Merchant
# merchant = {
#     'id': '98f9d65c-6dd8-46a9-8850-f5afd9a49013', 
#     'created_at': '2022-12-11T03:51:31Z', 
#     'updated_at': '2022-12-11T03:51:31Z', 
#     'name': 'Rivera, Ford and Haynes and Sons'
# }

# # Orders -- can be a purchase or refund
# orders= {
#     "id": "06489334-f6e7-4dd3-8cee-93c5cf061c5d",
#     "transactions": [
#         "7e805039-ae11-4ea4-885b-6dd8c5cde592"
#     ],
#     "created_at": "2023-01-13T15:58:00Z",
#     "updated_at": "2023-01-13T15:58:00Z",
#     "type": "SALE",
#     "items_data": [
#     {
#         "name": "Product 46",
#         "quantity": 1,
#         "unit_price": "82.36"
#     },
#     {
#         "name": "Product 384",
#         "quantity": 3,
#         "unit_price": "0.19"
#     },
#     {
#         "name": "Product 739",
#         "quantity": 10,
#         "unit_price": "61.87"
#     }
#     ],
#     "total_amount": "701.63",
#     "trace_id": "EXTERNAL_469903",
#     "parent_order": None,
#     "customer": "b6ef1278-35a4-44f3-b47f-4c9775bea770",
#     "merchant": "58abbef5-5fcb-40c4-94d6-767eadcbfe7b"
# }

# # Transaction - 
# txn = {
#     "id": "4d331ddc-f5c2-4e17-8ec2-5ad522c07559",
#     "created_at": "2023-01-13T16:06:40Z",
#     "updated_at": "2023-01-13T16:06:40Z",
#     "amount": "622.08",
#     "type": "SALE",
#     "customer": "0f83b0b7-3c49-415f-9d23-ba73d2eabe22",
#     "merchant": "b0c9a871-f9b3-411e-b713-b5b17287f956",
#     "order": "1605faff-853a-4240-aa57-2a4349ac3f58"
# }

# # input is the settlement amount for a given date, doesnt have to do with time within a day
# # ie; if a merchant sells 10 items online and refunds 2 orders what is the total settlement amount for that date 


# # possible settlement spec
# spec= {
#   "merchant_id": "string",
#   "settlement_date": "string",
#   "settlement_amount": "decimal",
#   "transaction_count": "integer",
#   "successful_transactions": "integer",
#   "failed_transactions": "integer",
#   "currency": "string",
#   "status": "string",
#   "details": [
#     {
#       "transaction_id": "string",
#       "amount": "decimal",
#       "status": "string",
#       "timestamp": "string"
#     }
#   ]
# }

# from decimal import Decimal

# from enum import Enum

# # ValueError: 'SALE' is not a valid TransactionType
# # Despite the OpenAPI spec:
# # PaymentTypeEnum:
# #       enum:
# #       - PURCHASE
# #       - REFUND
# #       type: string
# # I'm seeing the following additional type in the sample data: 'SALE'
# # Will assume for the purposes of this exercise that a PURCHASE ~= SALE
# class TransactionType(Enum):
#     PURCHASE = "PURCHASE"
#     REFUND = "REFUND"
#     SALE = "SALE"

# @dataclass
# class Transaction:
#     id: str
#     created_at: datetime
#     updated_at: datetime
#     amount: Decimal
#     type: TransactionType
#     customer: str
#     merchant: str
#     order: str

# @dataclass
# class SettlementResponse:
#     merchant_id: str
#     settlement_date: date
#     settlement_amount: Decimal
#     transaction_count: int
#     successful_sales: int
#     currency: str = "USD"
#     status: str = "completed"


# def calculate_settlement_amount(transactions: list[Transaction]) -> SettlementResponse:
#     """
#     Calculates the settlement amount given a list of transactions
#     """
#     settlement_amount = Decimal('0.00')
#     for transaction in transactions:
#         if transaction.type in (TransactionType.PURCHASE, TransactionType.SALE):
#             settlement_amount += transaction.amount
#         elif transaction.type == TransactionType.REFUND:
#             settlement_amount -= transaction.amount
#         else:
#             raise ValueError(f"Unexpected transaction type {transaction.type}, skipping to avoid erroneous calculations")
#     return settlement_amount


# def get_merchant_transactions(merchant_id: str, date: date):
#     """
#     Fetches all the transactions for a given merchant and date
#     """
#     merchant_transactions = []
#     next_url = "https://api-engine-dev.clerq.io/tech_assessment/transactions" 
#     while next_url:
#         try:
#             response = requests.get(
#                 next_url,
#                 params={
#                     "merchant": merchant_id,
#                     "created_at__gte": date.isoformat(),
#                     "created_at__lt": (date + timedelta(days=1)).isoformat()
#                 }, 
#                 timeout=5
#             )
#             response.raise_for_status()
#             data = response.json()
#             merchant_transactions.extend([
#                 Transaction(
#                     id=transaction['id'],
#                     created_at=datetime.fromisoformat(transaction['created_at'].rstrip('Z')),
#                     updated_at=datetime.fromisoformat(transaction['updated_at'].rstrip('Z')),
#                     amount=Decimal(transaction['amount']),
#                     type=TransactionType(transaction['type']),
#                     customer=transaction['customer'],
#                     merchant=transaction['merchant'],
#                     order=transaction['order']
#                 ) for transaction in data['results']
#             ])
#             next_url = data['next']
#         except Exception as e:
#             continue
        
#     return merchant_transactions

# def get_settlement(merchant_id: str, date: date) -> dict:
#     """
#     Returns settlement amount for the merchant on a given date.
#     """
#     # iso_date = date.isoformat()
#     # merchant_transactions = []
#     # merchant_transactions = requests.get(
#     #     'https://api-engine-dev.clerq.io/tech_assessment/transactions',
#     #     params={
#     #         "merchant": merchant_id,
#     #         "created_at__gte": date.isoformat(),
#     #         "created_at__lt": (date + timedelta(days=1)).isoformat()
#     #     }, 
#     #     timeout=5
#     # )

#     # Step 1 get all merchant transactions for date
#     transactions = get_merchant_transactions(merchant_id, date)
#     settlement_amount = calculate_settlement_amount(transactions) 
#     return settlement_amount


# # TODO Convert merchant string to uuid if they dont give merchant as uuid

# answer = get_settlement("b0c9a871-f9b3-411e-b713-b5b17287f956", date(2023, 1, 13))
# print(answer)


