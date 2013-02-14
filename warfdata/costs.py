from importlib import import_module

from warbdata.actions import ActionsData

from . import DataRepository


class CostsData(DataRepository):
    """DataRepository object for costs."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Cost = import_module('.Cost', package=self.package)

    def _get_cost(self, **kwargs):
        """Return a cost given a cost (other SQLA-Session) or a cost_id."""
        if 'cost' in kwargs:
            if not isinstance(kwargs['cost'], self.Cost.Cost):
                raise AttributeError('cost provided is not a wb-Cost')

            # Merging cost which may come from another session
            cost = self.session.merge(kwargs['cost'])

        elif 'cost_id' in kwargs:
            cost = self.session.query(self.Cost.Cost)\
                .filter(self.Cost.Cost.id == kwargs['cost_id'])\
                .one()

        else:
            raise TypeError('Cost informations (cost or cost_id) not provided')

        return cost

    def _pop_action(self, message=None, prestation=None):
        if not message or not prestation:
            raise TypeError('message or prestation not provided')

        self.actions_data.create(
            message=message.format(prestation.id))

    def create(self, pop_action=False, **kwargs):
        """Create and insert a cost in DB. Return this cost.

        Keyword arguments:
        see warbmodel.Cost.CostSchema

        """
        cost_schema = self.Cost.CostSchema(kwargs)  # Validate datas

        cost = self.Cost.Cost(**kwargs)
        self.session.add(cost)

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_COST_CREATE,
                prestation=kwargs['prestation'])

        # To get a full cost to return (get a working id)
        self.session.flush()

        return cost

    def update(self, pop_action=False, **kwargs):
        """Update a cost. Return False if there is no update or the updated
        cost.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        cost_id -- id of the cost to update (*)
        cost -- cost to update (*)
        amount -- new amount of the cost (**)
        reason -- new reason of the cost (**)

        * at least one is required
        ** see warbmodel.Cost.CostSchema for expected types

        """
        cost = self._get_cost(**kwargs)

        cost_dict = {k: v for k, v in cost.__dict__.items()
                     if k in cost.create_dict}
        new_cost_dict = cost_dict.copy()

        item_to_update = [item for item in cost.update_dict if item in kwargs]

        for item in item_to_update:
            new_cost_dict[item] = kwargs[item]

        self.Cost.CostSchema(new_cost_dict)

        for item in item_to_update:
            cost.__dict__[item] = kwargs[item]

        if new_cost_dict == cost_dict:
            return False

        self.session.flush()

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_COST_UPDATE, prestation=cost.prestation)

        return cost

    def remove(self, pop_action=False, **kwargs):
        """Remove a cost.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        cost_id -- id of the cost to remove (*)
        cost -- cost to remove (*)

        * at least one is required

        """
        cost = self._get_cost(**kwargs)
        prestation = cost.prestation
        self.session.delete(cost)

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_COST_REMOVE, prestation=prestation)
