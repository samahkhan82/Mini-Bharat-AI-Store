from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from .db import get_session
from .models import CreditProfile, Transaction, Inventory
import numpy as np

router = APIRouter(prefix='/credit')

@router.get('/score/{store_id}')
def credit_score(store_id: int, session: Session = Depends(get_session)):
    txs = session.exec(select(Transaction).where(Transaction.store_id==store_id)).all()
    if not txs:
        base = 0.4
    else:
        volumes = [abs(t.qty) for t in txs]
        base = min(0.9, 0.4 + np.log1p(sum(volumes))/10)
    invs = session.exec(select(Inventory).where(Inventory.store_id==store_id)).all()
    if invs:
        zeros = sum(1 for i in invs if i.quantity==0)
        pen = zeros/len(invs) * 0.2
    else:
        pen = 0.1
    score = max(0, min(1, base - pen))
    prof = session.exec(select(CreditProfile).where(CreditProfile.store_id==store_id)).first()
    if not prof:
        prof = CreditProfile(store_id=store_id, score=score)
        session.add(prof)
    else:
        prof.score = score
    session.commit()
    return {'store_id': store_id, 'score': float(score)}
