# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from . import DataRepository


class SalesmanData(DataRepository):
    """DataRepository object for salesmen."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Salesman = import_module('.Salesman', package=self._package)

    @db_method()
    def create(self, pop_action=False, **kwargs):
        """Create and insert a salesman in DB. Return this salesman.

        Keyword arguments:
        see warfinance.data.model.Salesman.SalesmanSchema

        """
        self.Salesman.SalesmanSchema(kwargs)

        salesman = self.Salesman.Salesman(**kwargs)
        self._dbsession.add(salesman)

        # Needed because of month.salesmen_com which is indexed using
        # salesman.id.
        self._expire.all_months()

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_CREATE
            self.action_data.create(message=msg)

        return salesman

    @db_method()
    def update(self, pop_action=False, **kwargs):
        """Update a salesman. Return False if there is no update or the updated
        salesman.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        salesman_id -- id of the salesman to update (*)
        salesman -- salesman to update (*)
        firstname -- new firstname of the salesman (**)
        lastname -- new lastname of the salesman (**)

        * at least one is required
        ** see warfinance.data.Salesman.SalesmanSchema for expected types

        """
        salesman = self._get.salesman(**kwargs)

        salesman_dict = {k: getattr(salesman, k) for k in salesman.create_dict
                         if getattr(salesman, k) is not None}
        new_salesman_dict = salesman_dict.copy()

        item_to_update = [i for i in salesman.update_dict if i in kwargs]

        for item in item_to_update:
            new_salesman_dict[item] = kwargs[item]

        self.Salesman.SalesmanSchema(new_salesman_dict)

        for item in item_to_update:
            setattr(salesman, item, kwargs[item])

        if new_salesman_dict == salesman_dict:
            return False

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_UPDATE
            self.action_data.create(message=msg)

        return salesman

    @db_method()
    def set_commissions_formulae(self, pop_action=False, **kwargs):
        """Set the commission formulae of a salesman. Return False if there is
        no update or the updated salesman.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        salesman_id -- id of the salesman to update (*)
        salesman -- salesman to update (*)
        commissions_formulae -- dict to set

        * at least one is required

        """
        if not 'commissions_formulae' in kwargs:
            raise TypeError('commissions_formulae missing')

        salesman = self._get.salesman(**kwargs)

        if kwargs['commissions_formulae'] == salesman.commissions_formulae:
            return False

        salesman.commissions_formulae = kwargs['commissions_formulae']

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_UPDATE
            self.action_data.create(message=msg)

        return salesman

    @db_method()
    def remove(self, pop_action=False, **kwargs):
        """Remove a salesman.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        salesman_id -- id of the salesman to remove (*)
        salesman -- salesman to remove (*)

        * at least one is required

        """
        salesman = self._get.salesman(**kwargs)

        for prestation in salesman.prestations:
            self._expire.prestation(prestation=prestation)

        self._dbsession.delete(salesman)

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_REMOVE
            self.action_data.create(message=msg)
