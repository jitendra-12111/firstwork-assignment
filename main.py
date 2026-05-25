from fastapi import FastAPI
from app.api import rules_router, companies_router, contracts_router

app = FastAPI()
app.include_router(rules_router)
app.include_router(contracts_router)
app.include_router(companies_router)