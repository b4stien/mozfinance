from sqlalchemy import Table, Column, ForeignKey, Integer, Unicode, PickleType
from sqlalchemy.orm import backref, relationship

from . import Base, Prestation


association_table = Table(
    'association_prestations_salesmen', Base.metadata,
    Column('salesman_id', Integer, ForeignKey('salesmen.id')),
    Column('prestation_id', Integer, ForeignKey('prestations.id'))
)


class Salesman(Base):
    __tablename__ = "salesmen"
    id = Column(Integer, primary_key=True)

    firstname = Column(Unicode(length=30))
    lastname = Column(Unicode(length=30))

    commissions_formulae = Column(PickleType)

    prestations = relationship(
        "Prestation",
        secondary=association_table,
        backref=backref('salesmen'))
