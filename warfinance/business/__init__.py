"""This package holds the business layer of warfinance.

It requires a valid model package (which is then provided to the DataRepository
in warfinance.data).

"""
from importlib import import_module

from sqlalchemy.orm.exc import NoResultFound

from warfinance.data import DataRepository

_ATTRIBUTES_DICT = {
    'month': {
        'revenu': 'month_revenu',
        'gross_margin': 'month_gross_margin',
        'net_margin': 'month_net_margin',
        'total_cost': 'month_total_cost',
    },
    'prestation': {
        'cost': 'prestation_cost',
        'margin': 'prestation_margin'
    },
    'year': {
        'net_margin': 'year_net_margin'
    }
}


class AbcBusinessWorker(DataRepository):
    """ABC for business worker objects.

    Provide a base with everything useful instancied.

    """

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self._attributes_dict = _ATTRIBUTES_DICT
        self.Prestation = import_module('.Prestation', package=self.package)
        self.Month = import_module('.Month', package=self.package)
        self.Salesman = import_module('.Salesman', package=self.package)

    def _get_computed_value(self, **kwargs):
        try:
            return DataRepository._get_computed_value(self, **kwargs)
        except NoResultFound:
            return None
