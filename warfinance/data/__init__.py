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

from warbase.data import DataRepository as WarbDataRepository
from warbase.data.actions import ActionsData


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

        self.actions_data = ActionsData(session=self.session,
                                        user=self.user)

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
        """Return a month given a month (other SQLA-Session) or a month_id."""
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
        required_list = ['date', 'breakeven']
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
