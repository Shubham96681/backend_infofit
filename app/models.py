from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Ticket(Base):
    __tablename__="tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable = False)
    details = Column(Text, nullable = False)
    status = Column(String(20), nullable=False, default="Open")