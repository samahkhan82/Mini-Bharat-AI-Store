from fastapi import FastAPI
from .db import create_db_and_tables
from .api_inventory import router as inventory_router
from .api_delivery import router as delivery_router
from .api_credit import router as credit_router
from .mock_integrations import get_offers, get_transactions

app = FastAPI(title='Mini Bharat AI Store')

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

app.include_router(inventory_router)
app.include_router(delivery_router)
app.include_router(credit_router)

@app.get('/offers')
def offers():
    return get_offers()

@app.get('/health')
def health():
    return {'status': 'ok'}





