# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

from mozbase.data import GetWorker as MozbaseGetWorker


class GetWorker(MozbaseGetWorker):

    def __init__(self, dbsession=None, package=None, **kwargs):
        MozbaseGetWorker.__init__(self, dbsession)
        self._package = package

    def salesman(self, salesman_id=None, salesman=None, **kwargs):
        """Return a salesman given a salesman or a salesman_id."""
        Salesman = import_module('.Salesman', package=self._package)
        if salesman:
            if not isinstance(salesman, Salesman.Salesman):
                raise AttributeError('salesman provided is not a wb-Salesman')

            return salesman

        elif salesman_id:
            return self._dbsession.query(Salesman.Salesman)\
                .filter(Salesman.Salesman.id == salesman_id)\
                .one()

        else:
            raise TypeError('Salesman informations not provided')

    def month(self, month_id=None, month=None, date=None, **kwargs):
        """Return a month given a month, a month_id or a date."""
        Month = import_module('.Month', package=self._package)
        if month:
            if not isinstance(month, Month.Month):
                raise AttributeError('month provided is not a wb-Month')

            return month

        elif month_id:
            return self._dbsession.query(Month.Month)\
                .filter(Month.Month.id == month_id)\
                .one()

        elif date:
            if not isinstance(date, datetime.date):
                raise AttributeError('date provided is not a datetime.date')

            return self._dbsession.query(Month.Month)\
                .filter(Month.Month.date == date)\
                .one()

        else:
            raise TypeError(
                'Month informations (month, month_id or date) not provided')

    def year(self, year_id=None, year=None, date=None, **kwargs):
        """Return a year (specific object) given a date or a year number."""
        Year = import_module('.FakeYear', package=self._package)

        if year:
            if not isinstance(year, Year.Year):
                raise AttributeError('year provided is not a correct Year')

            return year

        elif date:
            if not isinstance(date, datetime.date):
                raise AttributeError('year provided is not a datetime.date')
            if not date.month == 1 or not date.day == 1:
                raise AttributeError('date provided is not correct')
            year = Year.Year(date.year, self._dbsession)
            return year

        elif year_id:
            if not isinstance(year_id, int):
                raise AttributeError('year_id provided is not an int')
            year = Year.Year(year_id, self._dbsession)
            return year

        else:
            raise TypeError('year informations not provided')

    def prestation(self, prestation_id=None, prestation=None, **kwargs):
        """Return a prestation given a prestation or a prestation_id."""
        Prestation = import_module('.Prestation', package=self._package)
        if prestation:
            if not isinstance(prestation, Prestation.Prestation):
                raise AttributeError(
                    'prestation provided is not a wb-Prestation')

            return prestation

        elif prestation_id:
            return self._dbsession.query(Prestation.Prestation)\
                .filter(Prestation.Prestation.id == prestation_id).one()

        else:
            raise TypeError(
                'Prestation informations (prestation or prestation_id) not provided')

    def cost(self, cost_id=None, cost=None, **kwargs):
        """Return a cost (Cost) given a cost or a cost_id."""
        Cost = import_module('.Cost', package=self._package)

        if cost:
            if not isinstance(cost, Cost.Cost):
                raise AttributeError('cost provided is not a wb-Cost')

            return cost

        elif cost_id:
            return self._dbsession.query(Cost.Cost)\
                .filter(Cost.Cost.id == cost_id)\
                .one()

        else:
            raise TypeError(
                'CostPrestation informations (cost or cost_id) not provided')

    def prestation_salesman(self, **kwargs):
        """Get and return a PrestationSalesman object. Will raise an
        exception if no result is found.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self.prestation(**kwargs)
        salesman = self.salesman(**kwargs)

        PrestationSalesman = import_module(
            '.AssPrestationSalesman', package=self._package)
        presta_sm = presta.prestation_salesmen\
            .filter(PrestationSalesman.PrestationSalesman.salesman == salesman)\
            .one()

        return presta_sm
