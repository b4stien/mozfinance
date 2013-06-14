# -*- coding: utf-8 -*-
from importlib import import_module
import datetime

from mozbase.data import GetWorker as MozbaseGetWorker

import mozfinance


class GetWorker(MozbaseGetWorker):

    def __init__(self, dbsession=None, package=None, **kwargs):
        MozbaseGetWorker.__init__(self, dbsession)
        self._package = package

    def salesman(self, salesman_id=None, salesman=None, **kwargs):
        """Return a salesman given a salesman (other SQLA-Session) or
        a salesman_id."""
        Salesman = import_module('.Salesman', package=self._package)
        if salesman:
            if not isinstance(salesman, Salesman.Salesman):
                raise AttributeError('salesman provided is not a wb-Salesman')

            # Merging salesman which may come from another session
            return self._dbsession.merge(salesman)

        elif salesman_id:
            return self._dbsession.query(Salesman.Salesman)\
                .filter(Salesman.Salesman.id == salesman_id)\
                .one()

        else:
            raise TypeError('Salesman informations not provided')

    def month(self, month_id=None, month=None, date=None, **kwargs):
        """Return a month given a month (other SQLA-Session), a month_id or a
        date.

        """
        Month = import_module('.Month', package=self._package)
        if month:
            if not isinstance(month, Month.Month):
                raise AttributeError('month provided is not a wb-Month')

            # Merging month which may come from another session
            return self._dbsession.merge(month)

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
        """Return a year (ad-hoc object) given a date or a year number."""

        class Year():
            pass

        if year:
            # Does not work with ad-hoc objects
            # if not isinstance(kwargs['year'], Year):
            #     raise AttributeError('year provided is not an ad-hoc Year')
            return year

        elif date:
            if not isinstance(date, datetime.date):
                raise AttributeError('year provided is not a datetime.date')
            if not date.month == 1 or not date.day == 1:
                raise AttributeError('date provided is not correct')
            year = Year()
            setattr(year, 'id', date.year)
            setattr(year, 'date', date)
            return year

        elif year_id:
            if not isinstance(year_id, int):
                raise AttributeError('year_id provided is not an int')
            year_date = datetime.date(
                year=year_id,
                month=1,
                day=1)
            year = Year()
            setattr(year, 'id', year_date.year)
            setattr(year, 'date', year_date)
            return year

        else:
            raise TypeError('year informations not provided')

    def prestation(self, prestation_id=None, prestation=None, **kwargs):
        """Return a prestation given a prestation (other SQLA-Session) or a
        prestation_id."""
        Prestation = import_module('.Prestation', package=self._package)
        if prestation:
            if not isinstance(prestation, Prestation.Prestation):
                raise AttributeError(
                    'prestation provided is not a wb-Prestation')

            # Merging prestation which may come from another session
            return self._dbsession.merge(prestation)

        elif prestation_id:
            prestation_query = self._dbsession.query(Prestation.Prestation)\
                .filter(Prestation.Prestation.id == prestation_id)

            # Restrictions on the prestations that we will consider
            for query_filter in mozfinance.PRESTATIONS_FILTERS:
                prestation_query = prestation_query.filter(query_filter)

            return prestation_query.one()

        else:
            raise TypeError(
                'Prestation informations (prestation or prestation_id) not provided')

    def month_prestations(self, month_id=None, month=None, date=None, **kwargs):
        """Return the list of the prestations ot the given month."""
        month = self.month(month_id, month, date)

        prestations_query = month.prestations

        for query_filter in mozfinance.PRESTATIONS_FILTERS:
            prestations_query = prestations_query.filter(query_filter)

        prestations = prestations_query.all()

        return prestations

    def p_cost(self, p_cost_id=None, p_cost=None, **kwargs):
        """Return a p_cost (PrestationCost) given a p_cost (other SQLA-Session) or
        a pcost_id.
        """
        PrestationCost = import_module('.PrestationCost', package=self._package)

        if p_cost:
            if not isinstance(p_cost, PrestationCost.PrestationCost):
                raise AttributeError('pcost provided is not a wb-PrestationCost')

            # Merging cost which may come from another session
            return self._dbsession.merge(p_cost)

        elif p_cost_id:
            return self._dbsession.query(PrestationCost.PrestationCost)\
                .filter(PrestationCost.PrestationCost.id == p_cost_id)\
                .one()

        else:
            raise TypeError('PrestationCost informations (p_cost or p_cost_id) not provided')

    def prestation_salesman(self, **kwargs):
        """Get and return a PrestationSalesman object Will raise an exception if
        no result is found.

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

        PrestaSm = import_module('.PrestationSalesman', package=self._package)
        PrestaSm = PrestaSm.PrestationSalesman
        return self._dbsession.query(PrestaSm)\
            .filter(PrestaSm.salesman == salesman)\
            .filter(PrestaSm.prestation == presta)\
            .one()
