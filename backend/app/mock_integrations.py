import csv, os
from typing import List
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'mock_data')

def read_csv(name: str) -> List[dict]:
    path = os.path.join(DATA_DIR, name)
    with open(path) as f:
        return list(csv.DictReader(f))

def get_offers():
    return read_csv('offers.csv')

def get_transactions():
    return read_csv('transactions.csv')

def get_price_list_online():
    products = read_csv('products.csv')
    out = []
    for p in products:
        out.append({'sku': p['sku'], 'online_price': float(p.get('base_price',10))*1.2})
    return out
