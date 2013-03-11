from importlib import import_module

from . import DataRepository


class SalesmenData(DataRepository):
    """DataRepository object for salesmen."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Salesman = import_module('.Salesman', package=self.package)

    def create(self, pop_action=False, **kwargs):
        """Create and insert a salesman in DB. Return this salesman.

        Keyword arguments:
        see warfinance.data.model.Salesman.SalesmanSchema

        """
        salesman_schema = self.Salesman.SalesmanSchema(kwargs)

        salesman = self.Salesman.Salesman(**kwargs)
        self.session.add(salesman)

        self.session.commit()

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_CREATE
            self.actions_data.create(message=msg)

        return salesman

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
        salesman = self._get_salesman(**kwargs)

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

        self.session.commit()

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_UPDATE
            self.actions_data.create(message=msg)

        return salesman

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

        salesman = self._get_salesman(**kwargs)

        if kwargs['commissions_formulae'] == salesman.commissions_formulae:
            return False

        salesman.commissions_formulae = kwargs['commissions_formulae']

        self.session.commit()

        self._expire_salesman(salesman=salesman)

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_UPDATE
            self.actions_data.create(message=msg)

        return salesman

    def remove(self, pop_action=False, **kwargs):
        """Remove a salesman.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        salesman_id -- id of the salesman to remove (*)
        salesman -- salesman to remove (*)

        * at least one is required

        """
        salesman = self._get_salesman(**kwargs)
        self._expire_salesman(salesman=salesman)
        self.session.delete(salesman)
        self.session.commit()

        if pop_action:
            msg = self.Salesman.ACT_SALESMAN_REMOVE
            self.actions_data.create(message=msg)
