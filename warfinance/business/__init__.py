"""This package holds the business layer of WArFinance.

It requires a valid model package (which is then provided to the DataRepository
in warfinance.data).

"""
from sqlalchemy.orm.exc import NoResultFound

from warfinance.data import DataRepository


class AbcBusinessWorker(DataRepository):
    """ABC for business worker objects.

    Provide a base with everything useful instancied.

    """

    def _get_computed_value(self, **kwargs):
        try:
            return DataRepository._get_computed_value(self, **kwargs)
        except NoResultFound:
            return None


