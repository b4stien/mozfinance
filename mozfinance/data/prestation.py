# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from mozfinance.data import cost
from . import DataRepository


class PrestationData(DataRepository):
    """DataRepository object for prestations."""

    _patch_exports = ['set_selling_price', 'add_salesman', 'remove_salesman',
                      'set_salesman_ratio', 'set_salesman_formula', 'cost']

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Prestation = import_module('.Prestation', package=self._package)
        self.PrestationSalesman = import_module('.AssPrestationSalesman', package=self._package)

        self.cost = cost.CostPrestationData(**kwargs)

    def get(self, prestation_id=None, prestation=None, **kwargs):
        """Return a prestation.

        Arguments:
            prestation -- explicit (*)
            prestation_id -- id of the prestation (*)

        * at least one is required

        """
        presta = self._get.prestation(prestation_id, prestation)

        return presta

    @db_method
    def set_selling_price(self, prestation_id=None, prestation=None,
            selling_price=None, **kwargs):
        """Set the price of a prestation. Return False if there is no update or
        the updated prestation otherwise.

        Keyword arguments:
            prestation_id -- id of the prestation to update (*)
            prestation -- prestation to update (*)
            selling_price -- new selling_price of the prestation (**)

        * at least one is required
        ** see mozfinance.data.model.Prestation.PrestationSchema for expected types

        """
        presta = self._get.prestation(prestation_id, prestation)

        if not selling_price:
            raise TypeError('selling_price missing')

        if not isinstance(selling_price, float):
            raise AttributeError('selling_price isn\'t a float')

        if presta.selling_price == selling_price:
            return False

        presta.selling_price = selling_price

        self._expire.prestation(prestation=presta)

        return presta

    @db_method
    def add_salesman(self, prestation_id=None, prestation=None,
            salesman_id=None, salesman=None, **kwargs):
        """Add a salesman to a prestation and return True. If this salesman is
        already associated with the prestation, return False.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._get.prestation(prestation_id, prestation)
        salesman = self._get.salesman(salesman_id, salesman)

        if salesman in presta.salesmen:
            return False

        presta_sm = self.PrestationSalesman.PrestationSalesman()
        presta_sm.prestation = presta
        presta_sm.salesman = salesman
        presta_sm.formula = salesman.commissions_formulae[presta.sector][presta.category]

        self._dbsession.add(presta_sm)

        self._expire.prestation_salesmen(prestation=presta)

        return True

    @db_method
    def remove_salesman(self, **kwargs):
        """Remove a salesman from a prestation. If this salesman wasn't
        associated with the prestation, do nothing.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._get.prestation(**kwargs)
        salesman = self._get.salesman(**kwargs)

        if not salesman in presta.salesmen:
            return presta

        # We have to get the correct PrestationSalesman object.
        presta_sm = self._get.prestation_salesman(**kwargs)

        self._dbsession.delete(presta_sm)

        self._expire.prestation_salesmen(prestation=presta)

        return presta

    @db_method
    def set_salesman_ratio(self, **kwargs):
        """Set a custom ratio for a specific salesman/prestation. Return False
        if there is no update or True otherwise.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)
            ratio -- the ratio to set (or None)

        * at least one is required
        ** at least one is required

        """
        presta = self._get.prestation(**kwargs)

        if not 'ratio' in kwargs:
            raise TypeError('ratio missing')

        if not isinstance(kwargs['ratio'], float) and not kwargs['ratio'] is None:
            raise AttributeError('ratio isn\'t a float and isn\'t None')

        presta_sm = self._get.prestation_salesman(**kwargs)

        if presta_sm.ratio == kwargs['ratio']:
            return False

        presta_sm.ratio = kwargs['ratio']
        self._dbsession.add(presta_sm)

        self._expire.prestation_salesmen(prestation=presta)

        return True

    @db_method
    def set_salesman_formula(self, **kwargs):
        """Set a custom commission formula for a specific salesman/prestation.
        Return False if there is no update or True otherwise.

        If no formula is given, we use the default salesman's formula.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)
            formula -- the formula to set (or None)

        * at least one is required
        ** at least one is required

        """
        presta = self._get.prestation(**kwargs)
        salesman = self._get.salesman(**kwargs)

        if not 'formula' in kwargs:
            raise TypeError('formula missing')

        if not isinstance(kwargs['formula'], str) and not kwargs['formula'] is None:
            raise AttributeError('formula isn\'t a string and isn\'t None')

        presta_sm = self._get.prestation_salesman(**kwargs)

        if presta_sm.formula == kwargs['formula']:
            return False

        if kwargs['formula'] is None:
            presta_sm.formula = salesman.commissions_formulae[presta.category][presta.sector]
        else:
            presta_sm.formula = kwargs['formula']

        self._dbsession.add(presta_sm)

        self._expire.prestation_salesmen(prestation=presta)

        return presta
