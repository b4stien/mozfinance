from warbase.data.computed_values import ComputedValuesData

from . import AbcBusinessWorker


class ComputeWorker(AbcBusinessWorker):
    """BusinessWorker for computation. All recipes to compute values are stored
    here."""

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.compvalues_data = ComputedValuesData(**kwargs)

    def _get_or_compute(self, key, target_id, **kwargs):
        """Return a value (a real value and not a ComputedValue).

        Arguments:
        key -- key of the value (eg: "month:revenu").
               See warfinance.business.__ATTRIBUTES_DICT
        target_id -- id of the target

        Keyword arguments:
        instance -- target (SQLA-object)

        """
        # The "get" part of "get_or_compute"
        comp_value = self._get_computed_value(
            key=key,
            target_id=target_id)

        if comp_value is not None:
            return comp_value.value

        # And the "compute" part
        (instance_type, sep, prefix_key) = key.partition(':')
        method = self._attributes_dict[instance_type][prefix_key]

        # To avoid useless DB call.
        if 'instance' in kwargs:
            method_kwargs = {instance_type: kwargs['instance']}
        else:
            method_kwargs = {instance_type+'_id': target_id}

        return getattr(self, method)(**method_kwargs)

    def prestation_cost(self, **kwargs):
        """Compute and return the sum of all the costs of a prestation.

        Keyword arguments:
        prestation -- SQLA-Prestation (*)
        prestation_id -- id of the prestation (*)

        * at least one is required

        """
        presta = self._get_prestation(**kwargs)

        presta_cost = float(0)
        for cost in presta.costs:
            presta_cost += cost.amount

        # Storing value in DB
        self.compvalues_data.set(
            key='prestation:cost',
            target_id=presta.id,
            value=presta_cost)

        return presta_cost

    def prestation_margin(self, **kwargs):
        """Compute and return the margin of a prestation.

        Keyword arguments:
        prestation -- SQLA-Prestation (*)
        prestation_id -- id of the prestation (*)

        * at least one is required

        """
        presta = self._get_prestation(**kwargs)

        presta_cost = self._get_or_compute(
            'prestation:cost',
            presta.id,
            instance=presta)

        presta_margin = presta.selling_price - presta_cost

        # Storing value in DB
        self.compvalues_data.set(
            key='prestation:margin',
            target_id=presta.id,
            value=presta_margin)

        return presta_margin

    def month_revenu(self, **kwargs):
        """Compute and return the revenu of a month.

        Keyword arguments:
        month -- SQLA-Month (*)
        month_id -- id of the month (*)
        date -- datetime.date of the first day of the month (*)

        * at least one is required

        """
        month = self._get_month(**kwargs)

        Prestation = self.Prestation.Prestation  # abbr
        prestations = self.session.query(Prestation)\
            .filter(Prestation.date >= month.date)\
            .filter(Prestation.date < month.next_month())\
            .all()

        month_revenu = float(0)
        for presta in prestations:
            if presta.selling_price is not None:
                month_revenu += presta.selling_price

        self.compvalues_data.set(
            key='month:revenu',
            target_id=month.id,
            value=month_revenu)

        return month_revenu

    def month_gross_margin(self, **kwargs):
        """Compute and return the gross margin of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenu

        """
        month = self._get_month(**kwargs)

        month_revenu = self._get_or_compute(
            'month:revenu',
            month.id,
            instance=month)
        month_cost = self._get_or_compute(
            'month:total_cost',
            month.id,
            instance=month)

        month_gross_margin = month_revenu - month_cost
        self.compvalues_data.set(
            key='month:gross_margin',
            target_id=month.id,
            value=month_gross_margin)

        return month_gross_margin

    def month_total_cost(self, **kwargs):
        """Compute and return the sum of the costs of the prestations of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenu

        """
        month = self._get_month(**kwargs)

        Prestation = self.Prestation
        prestations = self.session.query(Prestation.Prestation)\
            .filter(Prestation.Prestation.date >= month.date)\
            .filter(Prestation.Prestation.date < month.next_month())\
            .all()

        month_cost = float(0)
        for presta in prestations:
            month_cost += self._get_or_compute(
                'prestation:cost',
                presta.id,
                instance=presta)

        self.compvalues_data.set(
            key='month:total_cost',
            target_id=month.id,
            value=month_cost)

        return month_cost

    def month_commission_base(self, **kwargs):
        """Compute and return the commission base of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenu

        """
        month = self._get_month(**kwargs)

        month_gross_margin = self._get_or_compute(
            'month:gross_margin',
            month.id,
            instance=month)

        if not month.breakeven:
            commission_base = float(0)
        else:
            commission_base = month_gross_margin - month.breakeven

        self.compvalues_data.set(
            key='month:commission_base',
            target_id=month.id,
            value=commission_base)

        return commission_base
