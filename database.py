from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from database_models import Request, Base

engine = create_engine(
    settings.database_source,
    connect_args={"check_same_thread": False},
)

Base.metadata.create_all(engine)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def add_request_record(user_id:int, search_query:str, shop:str) -> None:
    with Session() as session:
        new_request = Request(user_id=user_id, search_query=search_query, shop=shop)
        session.add(new_request)
        session.commit()

def check_if_user_in_base(user_id:int) -> bool:
    with Session() as session:
        user = session.query(Request).filter_by(user_id=user_id).first()
        
    if user is not None:
        return True
    return False

def retrieve_user_requests(user_id:int) -> List[Request]:
    with Session() as session:
        requests = session.query(Request).filter_by(user_id=user_id).all()
    return requests
