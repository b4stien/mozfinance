# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import backref, relationship

from mozbase.util.cache import cached_property

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

    # bidirectional attribute with "dynamic" loading.
    prestation_query = relationship(
        Prestation.Prestation,
        backref=backref('prestation_salesmen_query', cascade='all, delete-orphan', lazy='dynamic'))
    salesman_query = relationship(
        Salesman.Salesman,
        backref=backref('salesman_prestations_query', cascade='all, delete-orphan', lazy='dynamic'))

    prestation = relationship(
        Prestation.Prestation,
        backref=backref('prestation_salesmen', cascade='all, delete-orphan'))
    salesman = relationship(
        Salesman.Salesman,
        backref=backref('salesman_prestations', cascade='all, delete-orphan'))

    _key_store_key_template = 'prestation:{instance.prestation_id}:salesman:{instance.salesman_id}'

    @cached_property(
        'prestation:{instance.prestation.id}:salesman:{instance.salesman.id}:commission')
    def commission(self):
        """Compute and return the commission of this salesman regarding
        this prestation.

        """
        com_params = self.prestation.commissions_variables
        if not com_params:
            return float(0)

        # If prestation's margin or month's commission's base is
        # negative, there is no commission.
        if (self.prestation.margin <= float(0) or
            self.prestation.month.commission_base <= float(0)):
            return float(0)

        if not self.ratio is None:
            ratio = self.ratio

        else:
            # If ratio is not defined, we attribute a default "equal"
            # ratio.
            ratio = float(1) / float(self.prestation.prestation_salesmen_query.count())

        return eval(self.formula.format(**com_params)) * ratio
