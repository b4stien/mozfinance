# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from mozfinance.data import DataRepository


class SalesmanData(DataRepository):
    """DataRepository object for salesmen."""

    def __init__(self, bo=None):
        DataRepository.__init__(self, bo, managed_object_name='salesman')
        self.Salesman = import_module('.Salesman', package=self._package)
        self._managed_object = self.Salesman.Salesman

    @db_method
    def create(self, **kwargs):
        """Create and insert a salesman in DB. Return this salesman.

        Keyword arguments:
            see mozfinance.data.model.Salesman.SalesmanSchema

        """
        self.Salesman.SalesmanSchema(kwargs)

        salesman = self.Salesman.Salesman(**kwargs)
        self._dbsession.add(salesman)

        return salesman

    @db_method
    def update(self, salesman_id=None, salesman=None, **kwargs):
        """Update a salesman. Return False if there is no update or the updated
        salesman.

        Keyword arguments:
            salesman_id -- id of the salesman to update (*)
            salesman -- salesman to update (*)
            firstname -- new firstname of the salesman (**)
            lastname -- new lastname of the salesman (**)

        * at least one is required
        ** see mozfinance.data.Salesman.SalesmanSchema for expected types

        """
        salesman = self._get(salesman_id, salesman)

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

        return salesman

    @db_method
    def set_commissions_formulae(self, salesman_id=None, salesman=None,
            commissions_formulae=None):
        """Set the commission formulae of a salesman. Return False if there is
        no update or the updated salesman.

        Keyword arguments:
            salesman_id -- id of the salesman to update (*)
            salesman -- salesman to update (*)
            commissions_formulae -- dict to set

        * at least one is required

        """
        if commissions_formulae is None:
            raise TypeError('commissions_formulae missing')

        salesman = self._get(salesman_id, salesman)

        if commissions_formulae == salesman.commissions_formulae:
            return False

        salesman.commissions_formulae = commissions_formulae

        return salesman

    @db_method
    def remove(self, salesman_id=None, salesman=None):
        """Remove a salesman.

        Keyword arguments:
            salesman_id -- id of the salesman to remove (*)
            salesman -- salesman to remove (*)

        * at least one is required

        """
        salesman = self._get(salesman_id, salesman)

        for prestation in salesman.prestations:
            self._bo.prestation._expire(prestation=prestation)

        self._dbsession.delete(salesman)
