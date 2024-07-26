# acme_settlement_serivce
Exposes a settlement process for a merchants

Installation

Python version (I'm using builtin types, so 3.11+ is required)
```
❯ python --version
Python 3.11.9
```

Clone the repository:
```
git clone https://github.com/your-username/acme-settlement-service.git
cd acme-settlement-service
pip install -r requirements.txt
```

Run the application:

Due to my project structure (fastapi app lives in `/app` directory instead of root directory), please ensure you
have the correct "python.analysis.extraPaths" set in your [settings.json](.vscode/settings.json) or else vscode
linting/syntax highlighting will not work as expected.

Run using vscode (easiest):
Use the vscode [run/debug feature with the the configuration "Python: Module" selected](.vscode/launch.json)

Run using uvicorn cli:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```


Once the app is up and running, you can use the following command to ensure:
```
curl -X GET "http://localhost:8000/api/v1/settlement?merchant_id=b0c9a871-f9b3-411e-b713-b5b17287f956&settlement_date=2023-01-13"
```
and recieve the following response
```
{"merchant_id":"b0c9a871-f9b3-411e-b713-b5b17287f956","settlement_date":"2023-01-13","settlement_amount":"30787.34","transaction_count":46}%
```









