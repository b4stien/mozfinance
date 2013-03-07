from warfinance.data import costs, months, prestations, salesmen

from . import AbcBusinessWorker


class DataWorker(AbcBusinessWorker):

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.costs = costs.CostsData(**kwargs)
        self.months = months.MonthsData(**kwargs)
        self.prestations = prestations.PrestationsData(**kwargs)
        self.salesmen = salesmen.SalesmenData(**kwargs)
