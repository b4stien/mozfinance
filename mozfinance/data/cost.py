# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from . import DataRepository


class CostData(DataRepository):
    """DataRepository object for costs."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.CostClass = None
        self.CostSchema = None

    @db_method
    def create(self, **kwargs):
        """Create and insert a cost in DB. Return this cost.

        Keyword arguments:
            see CostSchema

        """
        # Validate datas
        self.CostSchema(kwargs)

        cost = self.CostClass(**kwargs)
        self._dbsession.add(cost)

        return cost

    @db_method
    def update(self, **kwargs):
        """Update a cost. Return False if there is no update or the updated
        cost.

        Keyword arguments:
            cost_id -- id of the cost to update (*)
            cost -- cost to update (*)
            amount -- new amount of the cost (**)
            reason -- new reason of the cost (**)

        """
        cost = self._get.cost(**kwargs)

        cost_dict = {k: getattr(cost, k) for k in cost.create_dict
                      if getattr(cost, k) is not None}
        new_cost_dict = cost_dict.copy()

        item_to_update = [item for item in cost.update_dict if item in kwargs]

        for item in item_to_update:
            new_cost_dict[item] = kwargs[item]

        self.CostSchema(new_cost_dict)

        for item in item_to_update:
            setattr(cost, item, kwargs[item])

        if new_cost_dict == cost_dict:
            return False

        return cost

    @db_method
    def remove(self, **kwargs):
        """Remove a cost.

        Keyword arguments:
            cost_id -- id of the pcost to remove (*)
            cost -- pcost to remove (*)

        * at least one is required

        """
        cost = self._get.cost(**kwargs)
        self._dbsession.delete(cost)


class CostPrestationData(CostData):
    """DataRepository object for prestation's costs."""

    def __init__(self, **kwargs):
        CostData.__init__(self, **kwargs)
        CostPrestation = import_module('.CostPrestation', package=self._package)
        self.CostClass = CostPrestation.CostPrestation
        self.CostSchema = CostPrestation.CostPrestationSchema

    def create(self, **kwargs):
        cost = CostData.create(self, **kwargs)
        self._expire.prestation(prestation=cost.prestation)
        return cost

    def update(self, **kwargs):
        cost = self._get.cost(**kwargs)
        will_return = CostData.update(self, **kwargs)
        self._expire.prestation(prestation=cost.prestation)
        return will_return

    def remove(self, **kwargs):
        cost = self._get.cost(**kwargs)
        prestation = cost.prestation
        CostData.remove(self, **kwargs)
        self._expire.prestation(prestation=prestation)


class CostMonthData(CostData):
    """DataRepository object for month's costs."""

    def __init__(self, **kwargs):
        CostData.__init__(self, **kwargs)
        CostMonth = import_module('.CostMonth', package=self._package)
        self.CostClass = CostMonth.CostMonth
        self.CostSchema = CostMonth.CostMonthSchema

    def create(self, **kwargs):
        cost = CostData.create(self, **kwargs)
        self._expire.month(month=cost.month)
        return cost

    def update(self, **kwargs):
        cost = self._get.cost(**kwargs)
        will_return = CostData.update(self, **kwargs)
        self._expire.month(month=cost.month)
        return will_return

    def remove(self, **kwargs):
        cost = self._get.cost(**kwargs)
        month = cost.month
        CostData.remove(self, **kwargs)
        self._expire.month(month=month)
