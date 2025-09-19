from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .db import get_session
from .models import Inventory, Product
from datetime import datetime, timedelta

router = APIRouter(prefix='/inventory')

@router.post('/update')
def update_inventory(store_id: int, product_id: int, qty_change: int, session: Session = Depends(get_session)):
    stmt = select(Inventory).where(Inventory.store_id==store_id, Inventory.product_id==product_id)
    inv = session.exec(stmt).first()
    if not inv:
        inv = Inventory(store_id=store_id, product_id=product_id, quantity=max(0, qty_change))
        session.add(inv)
    else:
        inv.quantity = max(0, inv.quantity + qty_change)
    inv.last_updated = datetime.utcnow().isoformat()
    if qty_change>0:
        inv.expiry_date = (datetime.utcnow().date() + timedelta(days=90)).isoformat()
    session.commit()
    return {'ok': True, 'inventory': {'store_id': inv.store_id, 'product_id': inv.product_id, 'quantity': inv.quantity, 'expiry_date': str(inv.expiry_date)}}

@router.get('/store/{store_id}')
def get_store_inventory(store_id: int, session: Session = Depends(get_session)):
    stmt = select(Inventory, Product).where(Inventory.store_id==store_id).join(Product, Product.id==Inventory.product_id)
    rows = session.exec(stmt).all()
    result = []
    for inv, prod in rows:
        result.append({'product': prod.name, 'sku': prod.sku, 'quantity': inv.quantity, 'expiry_date': str(inv.expiry_date)})
    return result
