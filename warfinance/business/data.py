from warfinance.data import prestation_costs, months, prestations, salesmen

from . import AbcBusinessWorker


class DataWorker(AbcBusinessWorker):

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.months = months.MonthsData(**kwargs)

        self.prestations = prestations.PrestationsData(**kwargs)
        setattr(
            self.prestations,
            'costs',
            prestation_costs.PrestationCostsData(**kwargs))

        self.salesmen = salesmen.SalesmenData(**kwargs)
