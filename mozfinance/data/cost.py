# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from . import DataRepository


class CostData(DataRepository):
    """Abstract DataRepository object for costs."""

    def __init__(self, bo=None, package=None):
        DataRepository.__init__(self, bo, package)
        self._CostClass = None
        self._CostSchema = None

    def _get(self, cost_id=None, cost=None):
        """Return a cost given a cost or a cost_id."""
        if cost:
            if not isinstance(cost, self._CostClass):
                raise AttributeError('cost provided is not a wb-Cost')

            return cost

        elif cost_id:
            return self._dbsession.query(self._CostClass)\
                .filter(self._CostClass.id == cost_id)\
                .one()

        else:
            raise TypeError(
                'CostPrestation informations (cost or cost_id) not provided')

    def get(self, cost_id=None, cost=None, **kwargs):
        """Return a cost. Can accept extra arguments."""
        return self._get(cost_id, cost)

    @db_method
    def create(self, **kwargs):
        """Create and insert a cost in DB. Return this cost.

        Keyword arguments:
            see _CostSchema

        """
        self._CostSchema(kwargs)

        cost = self._CostClass(**kwargs)
        self._dbsession.add(cost)

        return cost

    @db_method
    def update(self, cost_id=None, cost=None, **kwargs):
        """Update a cost. Return False if there is no update or the updated
        cost.

        Keyword arguments:
            cost_id -- id of the cost to update (*)
            cost -- cost to update (*)
            amount -- new amount of the cost (**)
            reason -- new reason of the cost (**)

        """
        cost = self._get(cost_id, cost)

        cost_dict = {k: getattr(cost, k) for k in cost.create_dict
                      if getattr(cost, k) is not None}
        new_cost_dict = cost_dict.copy()

        item_to_update = [item for item in cost.update_dict if item in kwargs]

        for item in item_to_update:
            new_cost_dict[item] = kwargs[item]

        self._CostSchema(new_cost_dict)

        for item in item_to_update:
            setattr(cost, item, kwargs[item])

        if new_cost_dict == cost_dict:
            return False

        return cost

    @db_method
    def remove(self, cost_id=None, cost=None):
        """Remove a cost.

        Keyword arguments:
            cost_id -- id of the cost to remove (*)
            cost -- cost to remove (*)

        * at least one is required

        """
        cost = self._get(cost_id, cost)
        self._dbsession.delete(cost)


class CostPrestationData(CostData):
    """DataRepository object for prestation's costs."""

    def __init__(self, bo=None, package=None):
        CostData.__init__(self, bo, package)
        CostPrestation = import_module('.CostPrestation', package=self._package)
        self._CostClass = CostPrestation.CostPrestation
        self._CostSchema = CostPrestation.CostPrestationSchema

    def create(self, prestation_id=None, prestation=None, **kwargs):
        presta = self._bo.prestation._get(prestation_id, prestation)
        kwargs['prestation'] = presta

        cost = CostData.create(self, **kwargs)
        self._bo.prestation._expire(prestation=presta)

        return cost

    def update(self, cost_id=None, cost=None, **kwargs):
        cost = self._get(cost_id, cost)
        kwargs['cost'] = cost

        will_return = CostData.update(self, **kwargs)
        self._bo.prestation._expire(prestation=cost.prestation)

        return will_return

    def remove(self, cost_id=None, cost=None):
        cost = self._get(cost_id, cost)
        prestation = cost.prestation
        CostData.remove(self, cost=cost)
        self._bo.prestation._expire(prestation=prestation)


class CostMonthData(CostData):
    """DataRepository object for month's costs."""

    def __init__(self, bo=None, package=None):
        CostData.__init__(self, bo, package)
        CostMonth = import_module('.CostMonth', package=self._package)
        self._CostClass = CostMonth.CostMonth
        self._CostSchema = CostMonth.CostMonthSchema

    def create(self, month_id=None, month=None, month_date=None,
               expire=True, **kwargs):
        month = self._bo.month._get(month_id, month, month_date)
        kwargs['month'] = month

        cost = CostData.create(self, **kwargs)
        if not expire:
            self._bo.month._expire(month=month)

        return cost

    def update(self, cost_id=None, cost=None, expire=True, **kwargs):
        cost = self._get(cost_id, cost)
        kwargs['cost'] = cost

        will_return = CostData.update(self, **kwargs)
        if not expire:
            self._bo.month._expire(month=cost.month)

        return will_return

    def remove(self, cost_id=None, cost=None, expire=True, **kwargs):
        cost = self._get(cost_id, cost)
        month = cost.month
        CostData.remove(self, cost=cost)
        if not expire:
            self._bo.month._expire(month=month)

    def actions_batch(self, month_id=None, month=None, create=None,
                      update=None, remove=None):
        """Perform a batch of actions over given month's costs.

        create/update/remove must be lists of dictonaries containing the
        arguments that will be passed to create/update/remove methods.

        Beware, only the given month will be expired. If some actions
        are performed over other months (for instance because a cost of
        another month has been given), these months won't be expired.

        Eg: actions_batch(
                month_id=2,
                remove=[{'cost_id': 2}, {'cost_id': 3}])

        Keyword Arguments:
            month -- explicit (*)
            month_id -- explicit (*)
            create -- list of create actions
            update -- list of update actions
            remove -- list of remove actions

        * at least one is required

        """
        month = self._bo.month._get(month_id, month)

        if create:
            for item in create:
                self.create(expire=False, commit=False, **item)

        if update:
            for item in update:
                self.update(expire=False, commit=False, **item)

        if remove:
            for item in remove:
                self.remove(expire=False, commit=False, **item)

        self._dbsession.commit()
        self._bo.month._expire(month=month)
