"""Populate DB from CSVs in ../mock_data
Usage: python -m app.sample_data_loader
"""
import csv, os
from sqlmodel import Session
from .db import engine, create_db_and_tables
from .models import Store, Product, Inventory, CreditProfile

create_db_and_tables()
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'mock_data')

def load():
    with Session(engine) as s:
        with open(os.path.join(DATA_DIR, 'stores.csv')) as f:
            for r in csv.DictReader(f):
                s.add(Store(name=r['name'], latitude=float(r['latitude']), longitude=float(r['longitude'])))
        s.commit()
        with open(os.path.join(DATA_DIR, 'products.csv')) as f:
            for r in csv.DictReader(f):
                s.add(Product(sku=r['sku'], name=r['name'], shelf_life_days=int(r.get('shelf_life_days',365))))
        s.commit()
        stores = s.exec("SELECT * FROM store").all()
        products = s.exec("SELECT * FROM product").all()
        for st in stores:
            for p in products:
                s.add(Inventory(store_id=st.id, product_id=p.id, quantity=50))
        s.commit()
        for st in stores:
            s.add(CreditProfile(store_id=st.id, score=0.5))
        s.commit()

if __name__ == '__main__':
    load()
    print('Seeded DB')
