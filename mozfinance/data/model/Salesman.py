# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Unicode, PickleType
from sqlalchemy.ext.associationproxy import association_proxy
from voluptuous import Schema, Required, All, Length

from . import Base


class Salesman(Base):
    __tablename__ = "salesmen"
    id = Column(Integer, primary_key=True)

    firstname = Column(Unicode(length=30))
    lastname = Column(Unicode(length=30))

    # Dict with prestation.category first and prestation.sector then.
    # Eg: com_form[presta.category][presta.sector]
    commissions_formulae = Column(PickleType)

    prestations = association_proxy('salesman_prestations', 'prestation')

    update_dict = set(['firstname', 'lastname'])  # For update purpose
    create_dict = set(['firstname', 'lastname'])


SalesmanSchema = Schema({
    Required('firstname'): All(unicode, Length(min=3, max=30)),
    Required('lastname'): All(unicode, Length(min=3, max=30))
})

ACT_SALESMAN_CREATE = u'Ajout d\'un commercial'
ACT_SALESMAN_UPDATE = u'Modification d\'un commercial'
ACT_SALESMAN_REMOVE = u'Suppression d\'un commercial'
