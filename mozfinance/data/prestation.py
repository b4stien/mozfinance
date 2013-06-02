# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from mozfinance.data import prestation_cost
from . import DataRepository


class PrestationData(DataRepository):
    """DataRepository object for prestations."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Prestation = import_module('.Prestation', package=self._package)
        self.PrestationSalesman = import_module('.PrestationSalesman', package=self._package)

        self.cost = prestation_cost.PrestationCostData(**kwargs)

    def get(self, compute=False, **kwargs):
        """Return a presta with additional attributes.

        Keyword arguments:
        prestation -- see mozfinance.data.DataRepository._get_prestation (*)
        prestation_id -- see mozfinance.data.DataRepository._get_prestation (*)
        compute -- (bool) Wether to compute missing attributes or not.

        * at least one is required

        """
        presta = self._get.prestation(**kwargs)

        presta = self._add_attributes('prestation', presta, compute)

        return presta

    @db_method()
    def set_selling_price(self, pop_action=False, **kwargs):
        """Set the price of a prestation. Return False if there is no update or
        the updated prestation otherwise.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation to update (*)
        prestation -- prestation to update (*)
        selling_price -- new selling_price of the prestation (**)

        * at least one is required
        ** see warfinance.data.model.Prestation.PrestationSchema for expected types

        """
        presta = self._get.prestation(**kwargs)

        if not 'selling_price' in kwargs:
            raise TypeError('selling_price missing')

        if not isinstance(kwargs['selling_price'], float):
            raise AttributeError('selling_price isn\'t a float')

        if presta.selling_price == kwargs['selling_price']:
            return False

        presta.selling_price = kwargs['selling_price']

        self._expire.prestation(prestation=presta)

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_SELLING_PRICE
            self.action_data.create(message=msg.format(presta.id))

        return presta

    @db_method()
    def add_salesman(self, pop_action=False, **kwargs):
        """Add a salesman to a prestation and return Rue. If this salesman is
        already associated with the prestation, return False.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation (*)
        prestation -- prestation (*)
        salesman_id -- salesman (**)
        salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._get.prestation(**kwargs)
        salesman = self._get.salesman(**kwargs)

        if salesman in presta.salesmen:
            return False

        presta_sm = self.PrestationSalesman.PrestationSalesman()
        presta_sm.prestation = presta
        presta_sm.salesman = salesman
        presta_sm.formula = salesman.commissions_formulae[presta.sector][presta.category]

        self._dbsession.add(presta_sm)

        self._expire.prestation_salesman(prestation=presta)

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_ADD_SALESMAN
            self.action_data.create(message=msg.format(presta.id))

        return True

    @db_method()
    def remove_salesman(self, pop_action=False, **kwargs):
        """Remove a salesman from a prestation. If this salesman wasn't
        associated with the prestation, do nothing.

        Keyword arguments:
        pop_action -- wether to pop an action or not
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

        self._expire.prestation_salesman(prestation=presta)

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_REMOVE_SALESMAN
            self.action_data.create(message=msg.format(presta.id))

        return presta

    @db_method()
    def set_salesman_ratio(self, pop_action=False, **kwargs):
        """Set a custom ratio for a specific salesman/prestation. Return False
        if there is no update or True otherwise.

        Keyword arguments:
        pop_action -- wether to pop an action or not
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

        self._expire.prestation_salesman(prestation=presta)

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_CUSTOM_RATIOS
            self.action_data.create(message=msg.format(presta.id))

        return True

    @db_method()
    def set_salesman_formula(self, pop_action=False, **kwargs):
        """Set a custom commission formula for a specific salesman/prestation.
        Return False if there is no update or True otherwise.

        If no formula is given, we use the default salesman's formula.

        Keyword arguments:
        pop_action -- wether to pop an action or not
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

        self._expire.prestation_salesman(prestation=presta)

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_CUSTOM_COM_FORMULAE
            self.action_data.create(message=msg.format(presta.id))

        return presta
