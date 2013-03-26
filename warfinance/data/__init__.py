"""This package holds the integrity layer of warfinance.

It requires a valid model package (which is provided to DataRepository). It
also provides a class to check wether the provided model package fits the
requirements or not.

"""
from importlib import import_module
import datetime

import locale
try:
    locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'fr_FR')

from sqlalchemy.orm.exc import NoResultFound

from warbase.data import DataRepository as WarbDataRepository
from warbase.data.actions import ActionsData
from warbase.data.computed_values import ComputedValuesData


class DataRepository(WarbDataRepository):
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    """

    def __init__(self, **kwargs):
        """Init a DataRepository object, ABC for other Data objects.

        Keyword arguments (all required):
        package -- package holding the models
        session -- SQLA-Session
        user -- user using the DataRepository

        """
        WarbDataRepository.__init__(self, **kwargs)

        if not 'package' in kwargs:
            raise TypeError('package not provided')

        import_module(kwargs['package'])

        self.package = kwargs['package']

        self.user = self._get_user(**kwargs)

        self.actions_data = ActionsData(**kwargs)
        self.computed_values = ComputedValuesData(**kwargs)

    def _get_salesman(self, **kwargs):
        """Return a salesman given a salesman (other SQLA-Session) or
        a salesman_id."""
        Salesman = import_module('.Salesman', package=self.package)
        if 'salesman' in kwargs:
            if not isinstance(kwargs['salesman'], Salesman.Salesman):
                raise AttributeError('salesman provided is not a wb-Salesman')

            # Merging salesman which may come from another session
            return self.session.merge(kwargs['salesman'])

        elif 'salesman_id' in kwargs:
            return self.session.query(Salesman.Salesman)\
                .filter(Salesman.Salesman.id == kwargs['salesman_id'])\
                .one()

        else:
            raise TypeError('Salesman informations not provided')

    def _get_month(self, **kwargs):
        """Return a month given a month (other SQLA-Session), a month_id or a
        date.

        """
        Month = import_module('.Month', package=self.package)
        if 'month' in kwargs:
            if not isinstance(kwargs['month'], Month.Month):
                raise AttributeError('month provided is not a wb-Month')

            # Merging month which may come from another session
            month = self.session.merge(kwargs['month'])

        elif 'month_id' in kwargs:
            month = self.session.query(Month.Month)\
                .filter(Month.Month.id == kwargs['month_id'])\
                .one()

        elif 'date' in kwargs:
            if not isinstance(kwargs['date'], datetime.date):
                raise AttributeError('date provided is not a datetime.date')

            month = self.session.query(Month.Month)\
                .filter(Month.Month.date == kwargs['date'])\
                .one()

        else:
            raise TypeError(
                'Month informations (month, month_id or date) not provided')

        return month

    def _get_year(self, **kwargs):
        """Return a year (ad-hoc object) given a date or a year number."""

        class Year():
            pass

        if 'year' in kwargs:
            # Does not work with ad-hoc objects
            # if not isinstance(kwargs['year'], Year):
            #     raise AttributeError('year provided is not an ad-hoc Year')
            year = kwargs['year']

        elif 'date' in kwargs:
            if not isinstance(kwargs['date'], datetime.date):
                raise AttributeError('year provided is not a datetime.date')
            if not kwargs['date'].month == 1 or not kwargs['date'].day == 1:
                raise AttributeError('date provided is not correct')
            year = Year()
            setattr(year, 'id', kwargs['date'].year)
            setattr(year, 'date', kwargs['date'])

        elif 'year_id' in kwargs:
            if not isinstance(kwargs['year_id'], int):
                raise AttributeError('year_id provided is not an int')
            year_date = datetime.date(
                year=kwargs['year_id'],
                month=1,
                day=1)
            year = Year()
            setattr(year, 'id', year_date.year)
            setattr(year, 'date', year_date)

        else:
            raise TypeError('year informations not provided')

        return year

    def _get_prestation(self, **kwargs):
        """Return a prestation given a prestation (other SQLA-Session) or a
        prestation_id."""
        Prestation = import_module('.Prestation', package=self.package)
        if 'prestation' in kwargs:
            if not isinstance(kwargs['prestation'],
                              Prestation.Prestation):
                raise AttributeError(
                    'prestation provided is not a wb-Prestation')

            # Merging prestation which may come from another session
            return self.session.merge(kwargs['prestation'])

        elif 'prestation_id' in kwargs:
            presta_id = kwargs['prestation_id']
            return self.session.query(Prestation.Prestation)\
                .filter(Prestation.Prestation.id == presta_id)\
                .one()

        else:
            raise TypeError(
                'Prestation informations (prestation or prestation_id) not provided')

    def _expire_prestation(self, **kwargs):
        presta = self._get_prestation(**kwargs)
        self.computed_values.expire(key='prestation:', target_id=presta.id)
        self._expire_month(date=presta.month_date())

    def _expire_month(self, **kwargs):
        try:
            month = self._get_month(**kwargs)
        except NoResultFound:
            return

        # To expire commissions
        Prestation = import_module('.Prestation', package=self.package)
        prestas = self.session.query(Prestation.Prestation)\
            .filter(Prestation.Prestation.date >= month.date)\
            .filter(Prestation.Prestation.date < month.next_month())\
            .all()
        for presta in prestas:
            self._expire_prestation_salesman(prestation=presta)

        self.computed_values.expire(key='month:', target_id=month.id)

        self._expire_year(year_id=month.date.year)

    def _expire_year(self, **kwargs):
        year = self._get_year(**kwargs)
        self.computed_values.expire(key='year:', target_id=year.id)

    def _expire_prestation_salesman(self, **kwargs):
        presta = self._get_prestation(**kwargs)
        self.computed_values.expire(key='prestation:salesman:', target_id=presta.id)
        self._expire_month_salesman(date=presta.month_date())

    def _expire_month_salesman(self, **kwargs):
        try:
            month = self._get_month(**kwargs)
        except NoResultFound:
            return
        self.computed_values.expire(key='month:salesman:', target_id=month.id)

    def _expire_salesman(self, **kwargs):
        salesman = self._get_salesman(**kwargs)
        self.computed_values.expire_key(key='month:salesman:{}'.format(salesman.id))
        self.computed_values.expire_key(key='prestation:salesman:{}'.format(salesman.id))


class ModelPackageChecker():
    """Check if provided model package fits the requirements."""

    def __init__(self, **kwargs):
        """Register the model package."""
        if not 'package' in kwargs:
            raise TypeError('package not provided')

        import_module(kwargs['package'])

        self.package = kwargs['package']

    def _test_cost(self):
        """Test the Cost object."""
        Cost = import_module('.Cost', package=self.package)
        dir_list = dir(Cost.Cost)
        required_list = ['amount', 'reason', 'prestation', 'prestation_id']
        for item in required_list:
            if not item in dir_list:
                raise TypeError('Cost\'s {} field missing'.format(item))

    def _test_month(self):
        """Test the Month object."""
        Month = import_module('.Month', package=self.package)
        dir_list = dir(Month.Month)
        required_list = ['date', 'cost']
        for item in required_list:
            if not item in dir_list:
                raise TypeError('Month\'s {} field missing'.format(item))

    def _test_prestation(self):
        """Test the Prestation object."""
        Prestation = import_module('.Prestation', package=self.package)
        dir_list = dir(Prestation.Prestation)
        required_list = ['date', 'client', 'category', 'sector',
                         'selling_price']
        for item in required_list:
            if not item in dir_list:
                raise TypeError('Prestation\'s {} field missing'.format(item))

    def _test_salesman(self):
        """Test the Salesman object."""
        Salesman = import_module('.Salesman', package=self.package)
        dir_list = dir(Salesman.Salesman)
        required_list = ['firstname', 'lastname', 'commissions_formulae',
                         'prestations']
        for item in required_list:
            if not item in dir_list:
                raise TypeError('Salesman\'s {} field missing'.format(item))

    def run(self):
        """Run the test."""
        self._test_cost()
        self._test_month()
        self._test_prestation()
        self._test_salesman()
        return True
