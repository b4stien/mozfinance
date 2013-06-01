import datetime

from sqlalchemy.orm.exc import NoResultFound

import mozfinance

from . import AbcBusinessWorker
from compute import ComputeWorker
from data import DataWorker


class GetWorker(AbcBusinessWorker):
    """BusinessWorker to get SQLA-objects with additional datas."""

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self._compute = ComputeWorker(**kwargs)
        self._data = DataWorker(**kwargs)

    def _add_attributes(self, instance_type, instance, compute):

        # dict of all the possible additional attributes
        attr_dict = self._attributes_dict[instance_type]

        for key in attr_dict:
            comp_value = self._cache.get(
                key='{}:{}:{}'.format(instance_type, instance.id, key))

            # The value of the additional attribute is in DB.
            if comp_value is not None:
                setattr(instance, key, comp_value)

            # The value is not in DB but "compute" is True
            elif compute:
                kwargs = {instance_type: instance}
                comp_value = getattr(self._compute, attr_dict[key])(**kwargs)
                setattr(instance, key, comp_value)

            # The value cannot be set
            else:
                setattr(instance, key, None)

        return instance

    def month(self, compute=False, create=False, **kwargs):
        """Return a month with additional attributes.

        Keyword arguments:
        month -- see mozfinance.data.DataRepository._get_month (*)
        month_id -- see mozfinance.data.DataRepository._get_month (*)
        date -- any datetime.date of the month
        compute -- (bool) Wether to compute missing attributes or not.
        create -- (bool) Wether to create a non-existent month or not.

        * at least one is required

        """
        # "cleanify" date provided.
        if 'date' in kwargs:
            if not isinstance(kwargs['date'], datetime.date):
                raise AttributeError('date provided is not a datetime.date')
            kw_date = kwargs['date']
            kwargs['date'] = datetime.date(
                year=kw_date.year,
                month=kw_date.month,
                day=1)

        try:
            month = self._get_month(**kwargs)
        except NoResultFound:
            if not create or not 'date' in kwargs:
                raise NoResultFound
            month = self._data.month.create(date=kwargs['date'])
            self._dbsession.commit()

        month = self._add_attributes('month', month, compute)

        Prestation = self.Prestation
        prestas_query = self._dbsession.query(Prestation.Prestation)\
            .filter(Prestation.Prestation.date >= month.date)\
            .filter(Prestation.Prestation.date < month.next_month())

        # Restrictions on the prestations that we will consider
        for query_filter in mozfinance.PRESTATIONS_FILTERS:
            prestas_query = prestas_query.filter(query_filter)

        prestas = prestas_query.order_by(Prestation.Prestation.date).all()
        setattr(month, 'prestations', prestas)

        return month

    def prestation(self, compute=False, **kwargs):
        """Return a presta with additional attributes.

        Keyword arguments:
        prestation -- see mozfinance.data.DataRepository._get_prestation (*)
        prestation_id -- see mozfinance.data.DataRepository._get_prestation (*)
        compute -- (bool) Wether to compute missing attributes or not.

        * at least one is required

        """
        presta = self._get_prestation(**kwargs)

        presta = self._add_attributes('prestation', presta, compute)

        return presta

    def year(self, compute=False, **kwargs):
        """Return a year (ad-hoc class) with additional attributes.

        Keyword arguments:
        date -- any datetime.date of the month (required)
        compute -- (bool) Wether to compute missing attributes or not.

        * at least one is required

        """
        if 'date' in kwargs:
            if not isinstance(kwargs['date'], datetime.date):
                raise AttributeError('date provided is not a datetime.date')

        year = self._get_year(year_id=kwargs['date'].year)

        year = self._add_attributes('year', year, compute)

        return year
