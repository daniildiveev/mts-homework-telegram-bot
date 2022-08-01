from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer)
    search_query = sa.Column(sa.String)
    shop = sa.Column(sa.String)

