"""This package holds the integrity layer of WArFinance.

It requires a valid model package (which is provided to DataRepository). It
also provides a class to check wether the provided model package fits the
requirements or not.

"""
from importlib import import_module

from sqlalchemy.orm.session import Session as SQLA_Session

from warbmodel import User, Application


class DataRepository():
    """ABC for data repository objects.

    Provide a base with a fully functionnal SQLA-Session.

    """

    def _get_user(self, **kwargs):
        """Return a user given a user (other SQLA-Session) or a user_id."""
        if 'user' in kwargs:
            if not isinstance(kwargs['user'], User.User):
                raise AttributeError('user provided is not a wb-User')

            # Merging user which may come from another session
            user = self.session.merge(kwargs['user'])

        elif 'user_id' in kwargs:
            user = self.session.query(User.User)\
                .filter(User.User.id == kwargs['user_id'])\
                .one()

        else:
            raise TypeError('User informations (user or user_id) not provided')

        return user

    def _get_application(self, **kwargs):
        """Return an application given an application (other SQLA-Session) or
        a application_id."""
        if 'application' in kwargs:
            if not isinstance(kwargs['application'], Application.Application):
                raise AttributeError('application provided is not a wb-User')

            # Merging application which may come from another session
            app = self.session.merge(kwargs['application'])

        elif 'application_id' in kwargs:
            app_id = kwargs['application_id']
            app = self.session.query(Application.Application)\
                .filter(Application.Application.id == app_id)\
                .one()

        else:
            raise TypeError('Application informations (application or \
                application_id) not provided')

        return app

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

        self.user = self._get_user(**kwargs)

        self.application = self._get_application(**kwargs)


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
