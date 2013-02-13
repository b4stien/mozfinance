"""This package holds the integrity layer of WArFinance.

It requires a valid model package (which is provided to DataRepository). It
also provides a class to check wether the provided model package fits the
requirements or not.

"""
from sqlalchemy.orm.session import Session as SQLA_Session
from importlib import import_module


class DataRepository():
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    """

    def __init__(self, **kwargs):
        """Init a SQLA-Session."""
        if not 'session' in kwargs:
            raise TypeError('session not provided')

        if not isinstance(kwargs['session'], SQLA_Session):
            raise AttributeError('session provided is not a SQLA-Session')

        self.session = kwargs['session']

        if not 'package' in kwargs:
            raise TypeError('package not provided')

        import_module(kwargs['package'])

        self.package = kwargs['package']


class ModelPackageChecker():
    """Check if provided model package fits the requirements."""

    def __init__(self, **kwargs):
        """Register the model package."""
        if not 'package' in kwargs:
            raise TypeError('package not provided')

        import_module(kwargs['package'])

        self.package = kwargs['package']

    def _test_action(self):
        """Test the Action object."""
        Action = import_module('.Action', package=self.package)
        dir_list = dir(Action.Action)
        required_list = ['datetime', 'message', 'created_by_id', 'created_by',
                         'application_id', 'application']
        for item in required_list:
            if not item in dir_list:
                raise TypeError('Action\'s {} field missing'.format(item))

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
        self._test_action()
        self._test_cost()
        self._test_month()
        self._test_prestation()
        self._test_salesman()
        return True
