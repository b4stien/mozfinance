from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import backref, relationship

from . import Base, Prestation, Salesman


class PrestationSalesman(Base):
    __tablename__ = 'prestations_salesmen'
    prestation_id = Column(
        Integer,
        ForeignKey('prestations.id'),
        primary_key=True)
    salesman_id = Column(
        Integer,
        ForeignKey('salesmen.id'),
        primary_key=True)

    ratio = Column(Float)
    formula = Column(String)

    # bidirectional attribute
    prestation = relationship(
        Prestation.Prestation,
        backref=backref("prestation_salesmen"))
    salesman = relationship(
        Salesman.Salesman,
        backref=backref("salesman_prestations"))
