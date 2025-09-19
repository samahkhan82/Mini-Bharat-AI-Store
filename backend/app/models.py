from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    latitude: float
    longitude: float

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str
    name: str
    shelf_life_days: Optional[int] = 365

class Inventory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int
    product_id: int
    quantity: int
    last_updated: Optional[str] = None
    expiry_date: Optional[date] = None

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int
    product_id: int
    qty: int
    price: float
    timestamp: Optional[str] = None

class Delivery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str
    store_id: int
    status: str = "booked"
    pickup_lat: Optional[float] = None
    pickup_lng: Optional[float] = None
    drop_lat: Optional[float] = None
    drop_lng: Optional[float] = None
    assigned_truck_id: Optional[str] = None

class CreditProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int
    score: float = 0.0
    last_updated: Optional[str] = None
