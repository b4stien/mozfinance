# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from . import DataRepository


class PrestationCostData(DataRepository):
    """DataRepository object for costs."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.PrestationCost = import_module('.PrestationCost', package=self._package)

    def _pop_action(self, message=None, prestation=None):
        if not message or not prestation:
            raise TypeError('message or prestation not provided')

        self.action_data.create(
            message=message.format(prestation.id))

    @db_method()
    def create(self, pop_action=False, **kwargs):
        """Create and insert a pcost in DB. Return this pcost.

        Keyword arguments:
        see warfinance.data.model.PrestationCost.PrestationCostSchema

        """
        # Validate datas
        self.PrestationCost.PrestationCostSchema(kwargs)

        pcost = self.PrestationCost.PrestationCost(**kwargs)
        self._dbsession.add(pcost)

        self._expire.prestation(prestation=pcost.prestation)

        if pop_action:
            self._pop_action(
                message=self.PrestationCost.ACT_PRESTATION_COST_CREATE,
                prestation=kwargs['prestation'])

        return pcost

    @db_method()
    def update(self, pop_action=False, **kwargs):
        """Update a pcost. Return False if there is no update or the updated
        pcost.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        p_cost_id -- id of the pcost to update (*)
        p_cost -- pcost to update (*)
        amount -- new amount of the pcost (**)
        reason -- new reason of the pcost (**)

        * at least one is required
        ** see warfinance.data.model.PrestationCost.PrestationCostSchema

        """
        pcost = self._get.p_cost(**kwargs)

        pcost_dict = {k: getattr(pcost, k) for k in pcost.create_dict
                      if getattr(pcost, k) is not None}
        new_pcost_dict = pcost_dict.copy()

        item_to_update = [item for item in pcost.update_dict if item in kwargs]

        for item in item_to_update:
            new_pcost_dict[item] = kwargs[item]

        self.PrestationCost.PrestationCostSchema(new_pcost_dict)

        for item in item_to_update:
            setattr(pcost, item, kwargs[item])

        if new_pcost_dict == pcost_dict:
            return False

        self._expire.prestation(prestation=pcost.prestation)

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_PRESTATION_COST_UPDATE,
                prestation=pcost.prestation)

        return pcost

    @db_method()
    def remove(self, pop_action=False, **kwargs):
        """Remove a pcost.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        p_cost_id -- id of the pcost to remove (*)
        p_cost -- pcost to remove (*)

        * at least one is required

        """
        pcost = self._get.p_cost(**kwargs)
        prestation = pcost.prestation
        self._dbsession.delete(pcost)

        self._expire.prestation(prestation=prestation)

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_PRESTATION_COST_REMOVE,
                prestation=prestation)