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
        'cost': 'month_cost',
        'prestation_count': 'month_prestation_count',
        'commission_base': 'month_commission_base',
    },
    'prestation': {
        'cost': 'prestation_cost'
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

    def _get_computed_value(self, **kwargs):
        try:
            return DataRepository._get_computed_value(self, **kwargs)
        except NoResultFound:
            return None


