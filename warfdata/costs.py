from importlib import import_module

from warbdata.actions import ActionsData

from . import DataRepository


class CostsData(DataRepository):
    """DataRepository object for costs."""

    def create(self, pop_action=False, **kwargs):
        """Create and insert a cost in DB.

        Keyword arguments:
        see warbmodel.Application.CostSchema

        """
        Cost = import_module('.Cost', package=self.package)
        cost_schema = Cost.CostSchema(kwargs)  # Validate datas

        cost = Cost.Cost(**kwargs)
        self.session.add(cost)

        if pop_action:
            actions_data = ActionsData(session=self.session, user=self.user)
            actions_data.create(
                message=Cost.ACT_COST_CREATE.format(kwargs['prestation'].id),
                application=self.application)

        # To get a full application to return (get a working id)
        self.session.flush()

        return cost
