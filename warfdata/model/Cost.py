from sqlalchemy import Column, ForeignKey, Integer, Float, Unicode
from sqlalchemy.orm import backref, relationship

from . import Base, Prestation


class Cost(Base):
    __tablename__ = "costs"
    id = Column(Integer, primary_key=True)

    amount = Column(Float)
    reason = Column(Unicode(length=30))

    prestation_id = Column(Integer, ForeignKey('prestations.id'))
    prestation = relationship("Prestation", backref=backref('costs'))
