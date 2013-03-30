from importlib import import_module

from . import DataRepository


class PrestationCostsData(DataRepository):
    """DataRepository object for costs."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.PrestationCost = import_module('.PrestationCost', package=self.package)

    def _get_pcost(self, **kwargs):
        """Return a pcost (PrestationCost) given a pcost (other SQLA-Session) or
        a pcost_id.
        """
        if 'pcost' in kwargs:
            if not isinstance(kwargs['pcost'], self.PrestationCost.PrestationCost):
                raise AttributeError('pcost provided is not a wb-PrestationCost')

            # Merging cost which may come from another session
            pcost = self.session.merge(kwargs['pcost'])

        elif 'pcost_id' in kwargs:
            pcost = self.session.query(self.PrestationCost.PrestationCost)\
                .filter(self.PrestationCost.PrestationCost.id == kwargs['pcost_id'])\
                .one()

        else:
            raise TypeError('PrestationCost informations (pcost or pcost_id) not provided')

        return pcost

    def _pop_action(self, message=None, prestation=None):
        if not message or not prestation:
            raise TypeError('message or prestation not provided')

        self.actions_data.create(
            message=message.format(prestation.id))

    def create(self, pop_action=False, **kwargs):
        """Create and insert a pcost in DB. Return this pcost.

        Keyword arguments:
        see warfinance.data.model.PrestationCost.PrestationCostSchema

        """
        # Validate datas
        pcost_schema = self.PrestationCost.PrestationCostSchema(kwargs)

        pcost = self.PrestationCost.PrestationCost(**kwargs)
        self.session.add(pcost)

        self.session.commit()

        self._expire_prestation(prestation=pcost.prestation)

        if pop_action:
            self._pop_action(
                message=self.PrestationCost.ACT_PRESTATION_COST_CREATE,
                prestation=kwargs['prestation'])

        return pcost

    def update(self, pop_action=False, **kwargs):
        """Update a pcost. Return False if there is no update or the updated
        pcost.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        pcost_id -- id of the pcost to update (*)
        pcost -- pcost to update (*)
        amount -- new amount of the pcost (**)
        reason -- new reason of the pcost (**)

        * at least one is required
        ** see warfinance.data.model.PrestationCost.PrestationCostSchema

        """
        pcost = self._get_pcost(**kwargs)

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

        self.session.commit()

        self._expire_prestation(prestation=pcost.prestation)

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_PRESTATION_COST_UPDATE,
                prestation=pcost.prestation)

        return pcost

    def remove(self, pop_action=False, **kwargs):
        """Remove a pcost.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        pcost_id -- id of the pcost to remove (*)
        pcost -- pcost to remove (*)

        * at least one is required

        """
        pcost = self._get_pcost(**kwargs)
        prestation = pcost.prestation
        self.session.delete(pcost)
        self.session.commit()

        self._expire_prestation(prestation=prestation)

        if pop_action:
            self._pop_action(
                message=self.Cost.ACT_PRESTATION_COST_REMOVE,
                prestation=prestation)
