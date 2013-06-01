from mozfinance.data import prestation_cost, month, prestation, salesman

from . import AbcBusinessWorker


class DataWorker(AbcBusinessWorker):

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.month = month.MonthData(**kwargs)

        self.prestation = prestation.PrestationData(**kwargs)
        setattr(
            self.prestation,
            'cost',
            prestation_cost.PrestationCostData(**kwargs))

        self.salesman = salesman.SalesmanData(**kwargs)
