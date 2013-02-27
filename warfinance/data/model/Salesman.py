# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, ForeignKey, Integer, Unicode, PickleType
from sqlalchemy.orm import backref, relationship
from voluptuous import Schema, Required, All, Length

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

    update_dict = set(['firstname', 'lastname'])  # For update purpose
    create_dict = set(['firstname', 'lastname'])


SalesmanSchema = Schema({
    Required('firstname'): All(unicode, Length(min=3, max=30)),
    Required('lastname'): All(unicode, Length(min=3, max=30))
})

ACT_SALESMAN_CREATE = u'Ajout d\'un commercial'
ACT_SALESMAN_UPDATE = u'Modification d\'un commercial'
ACT_SALESMAN_REMOVE = u'Suppression d\'un commercial'
