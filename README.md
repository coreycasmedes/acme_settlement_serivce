# acme_settlement_serivce
Exposes a settlement process for a merchants

Installation

Clone the repository:
```
git clone https://github.com/your-username/acme-settlement-service.git
cd acme-settlement-service
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






