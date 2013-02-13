from sqlalchemy import Column, Integer, Date, Float

from . import Base


class Month(Base):
    __tablename__ = "months"
    id = Column(Integer, primary_key=True)

    date = Column(Date, index=True)  # First day of the month
    breakeven = Column(Float)
