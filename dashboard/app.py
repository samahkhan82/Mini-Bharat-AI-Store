import streamlit as st
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(page_title='Mini Bharat Dashboard')

st.title('Mini Bharat — Data Intelligence')

@st.cache_data
def load_tables():
    stores_df = pd.read_csv('../backend/mock_data/stores.csv')
    products_df = pd.read_csv('../backend/mock_data/products.csv')
    transactions_df = pd.read_csv('../backend/mock_data/transactions.csv')
    return stores_df, products_df, transactions_df

stores_df, products_df, transactions_df = load_tables()

st.subheader('Forecast demand for 3 products across 5 stores')
prod_ids = products_df['sku'].tolist()[:3]
forecast_horizon = 3
for sku in prod_ids:
    st.write(f'Product: {sku}')
    series = np.maximum(0, np.random.poisson(3, size=30))
    ma = pd.Series(series).rolling(7, min_periods=1).mean().iloc[-1]
    forecast = [float(ma) for _ in range(forecast_horizon)]
    st.write('3-day forecast (units/day):', forecast)

st.subheader('Identify expiry risks and suggest reorder points')
merged = []
for _, row in products_df.iterrows():
    if row['shelf_life_days'] < 180:
        merged.append((row['sku'], 'short shelf life'))
st.write('Products with short shelf life:', merged)

st.subheader('Compare local vs online pricing (top 10 items)')
local = products_df[['sku','base_price']].copy()
local['online_price'] = local['base_price']*1.2
st.dataframe(local.head(10))

st.subheader('Optimize delivery routes for 10 orders')
orders = []
for i in range(10):
    r = stores_df.sample(1).iloc[0]
    orders.append({'order_id': f'ord{i+1}', 'lat': r['latitude']+np.random.normal(0,0.02), 'lng': r['longitude']+np.random.normal(0,0.02)})

st.write('Orders sample:')
st.write(orders[:5])

def haversine(lat1, lon1, lat2, lon2):
    R=6371
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2-lat1)
    dl = radians(lon2-lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dl/2)**2
    return 2*R*atan2(sqrt(a), sqrt(1-a))

route = []
cur = orders[0]
unvisited = orders[1:]
route.append(cur)
while unvisited:
    nxt = min(unvisited, key=lambda o: haversine(cur['lat'], cur['lng'], o['lat'], o['lng']))
    unvisited.remove(nxt)
    route.append(nxt)
    cur = nxt

st.write('Planned route (naive NN):')
st.write([o['order_id'] for o in route])

st.markdown('---')
st.write('This dashboard uses simple heuristics for demonstration. For production use, plug real transactions and use stronger forecasting (Prophet / LSTM) and route optimization (OR-Tools).')
