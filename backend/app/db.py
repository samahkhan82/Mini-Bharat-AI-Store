from sqlmodel import SQLModel, create_engine, Session
import os
DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'mini_bharat.db')
DB_URL = f'sqlite:///{DB_FILE}'
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
