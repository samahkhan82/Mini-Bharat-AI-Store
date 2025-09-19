from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .db import get_session
from .models import Delivery, Store
import math

router = APIRouter(prefix='/delivery')

def haversine(lat1, lon1, lat2, lon2):
    R=6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2-lat1)
    dlambda = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.asin(math.sqrt(a))

@router.post('/book')
def book_delivery(store_id: int, drop_lat: float, drop_lng: float, order_id: str, session: Session = Depends(get_session)):
    stores = session.exec(select(Store)).all()
    if not stores:
        raise HTTPException(status_code=400, detail='No stores/trucks')
    best = min(stores, key=lambda s: haversine(s.latitude, s.longitude, drop_lat, drop_lng))
    deliv = Delivery(order_id=order_id, store_id=store_id, status='assigned', pickup_lat=best.latitude, pickup_lng=best.longitude, drop_lat=drop_lat, drop_lng=drop_lng, assigned_truck_id=f'truck_{best.id}')
    session.add(deliv)
    session.commit()
    return {'ok': True, 'delivery': {'order_id': deliv.order_id, 'assigned_truck_id': deliv.assigned_truck_id, 'status': deliv.status}}

@router.post('/optimize')
def optimize_route(orders: list, session: Session = Depends(get_session)):
    if not orders:
        return []
    unvisited = orders.copy()
    route = []
    cur = unvisited.pop(0)
    route.append(cur)
    while unvisited:
        nxt = min(unvisited, key=lambda o: haversine(cur['lat'], cur['lng'], o['lat'], o['lng']))
        unvisited.remove(nxt)
        route.append(nxt)
        cur = nxt
    return {'route': route}
