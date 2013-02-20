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
        see warbmodel.Salesman.SalesmanSchema

        """
        salesman_schema = self.Salesman.SalesmanSchema(kwargs)

        salesman = self.Salesman.Salesman(**kwargs)
        self.session.add(salesman)

        self.session.flush()

        if pop_action:
            msg = self.Prestation.ACT_SALESMAN_CREATE
            self.actions_data.create(message=msg)

        self.session.flush()

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
        ** see warbmodel.Salesman.SalesmanSchema for expected types

        """
        salesman = self._salesman_cost(**kwargs)

        salesman_dict = {k: v for k, v in salesman.__dict__.items()
                         if k in salesman.create_dict}
        new_salesman_dict = salesman_dict.copy()

        item_to_update = [i for i in salesman.update_dict if i in kwargs]

        for item in item_to_update:
            new_salesman_dict[item] = kwargs[item]

        self.Salesman.SalesmanSchema(new_salesman_dict)

        for item in item_to_update:
            salesman.__dict__[item] = kwargs[item]

        if new_salesman_dict == cost_dict:
            return False

        self.session.flush()

        if pop_action:
            msg = self.Prestation.ACT_SALESMAN_UPDATE
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
        salesman = self._salesman_cost(**kwargs)
        self.session.delete(salesman)

        if pop_action:
            msg = self.Prestation.ACT_SALESMAN_REMOVE
            self.actions_data.create(message=msg)
