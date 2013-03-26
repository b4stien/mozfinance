import datetime

from sqlalchemy.orm.exc import NoResultFound

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

        if presta.selling_price:
            presta_margin = presta.selling_price - presta_cost
        else:
            presta_margin = float(0)

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

    def month_net_margin(self, **kwargs):
        """Compute and return the net margin of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenu

        """
        month = self._get_month(**kwargs)

        month_gross_margin = self._get_or_compute(
            'month:gross_margin',
            month.id,
            instance=month)

        if not month.cost:
            month_net_margin = float(0)
        else:
            month_net_margin = month_gross_margin - month.cost

        self.compvalues_data.set(
            key='month:net_margin',
            target_id=month.id,
            value=month_net_margin)

        return month_net_margin

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

    def year_net_margin(self, **kwargs):
        """Compute and return the comulated net margin of the year_net_margin

        Keyword arguments:
        date -- Date of the first day of the year
        year_id -- Fake id, year as an int"""

        year = self._get_year(**kwargs)

        now_date = datetime.datetime.now().date()

        net_margin = float(0)

        for i in range(12):
            month_date = datetime.date(
                year=year.date.year,
                month=i+1,
                day=1)

            # We don't go into the future !
            if month_date > now_date:
                break

            # If the month is not found, we continue
            try:
                m = self._get_month(date=month_date)
            except NoResultFound:
                continue

            month_net_margin = self._get_or_compute(
                'month:net_margin', m.id, instance=m)

            net_margin += month_net_margin

        self.compvalues_data.set(
            key='year:net_margin',
            target_id=year.id,
            value=net_margin)

        return net_margin

    def _get_commission_params(self, **kwargs):
        """Compute and return a dict with all the commission params.

        Keyword arguments:
        prestation -- SQLA-Prestation (*)
        prestation_id -- id of the prestation (*)
        compute -- wether to compute missing data or not

        * at least one is required

        """
        p = self._get_prestation(**kwargs)
        m = self._get_month(date=p.month_date())
        com_params = {
            'm_ca': self._get_or_compute('month:revenu', m.id, instance=m),
            'm_mb': self._get_or_compute('month:gross_margin', m.id, instance=m),
            'm_mn': self._get_or_compute('month:net_margin', m.id, instance=m),
            'm_tc': self._get_or_compute('month:total_cost', m.id, instance=m),
            'm_ff': m.cost,
            'y_mn': self._get_or_compute('year:net_margin', m.date.year),
            'p_c': self._get_or_compute('prestation:cost', p.id, instance=p),
            'p_m': self._get_or_compute('prestation:margin', p.id, instance=p),
            'p_pv': p.selling_price,
        }
        for param in com_params:
            if not isinstance(com_params[param], float):
                return False
        return com_params

    def prestation_salesmen(self, compute=False, **kwargs):
        """Compute and return a dict indexed by the salesman.id of the salesmen
        of the prestation.

        Not optimized yet (not the same process than previous computation)

        Keyword arguments:
        prestation -- SQLA-Prestation (*)
        prestation_id -- id of the prestation (*)
        compute -- wether to compute missing data or not

        * at least one is required

        """
        presta = self._get_prestation(**kwargs)
        salesmen_dict = {}

        for salesman in presta.salesmen:

            if not presta.custom_ratios:
                ratio = float(1) / float(len(presta.salesmen))
            elif salesman.id in presta.custom_ratios:
                ratio = presta.custom_ratios[salesman.id]
            else:
                ratio = float(1)
            formula = salesman.commissions_formulae[presta.category][presta.sector]
            salesman_dict = {
                'formula': formula,
                'ratio': ratio
            }

            # This is because we cannot store Pickle in ComputedValue from now
            comp_value = self._get_computed_value(
                key='prestation:salesman:{}'.format(salesman.id),
                target_id=presta.id)
            if comp_value is not None:
                salesman_dict['commission'] = comp_value.value
                salesmen_dict[salesman.id] = salesman_dict
                continue

            if not compute:
                salesmen_dict[salesman.id] = False
                continue

            # If we can't get all params
            com_params = self._get_commission_params(prestation=presta)
            if not com_params:
                salesmen_dict[salesman.id] = False
                continue

            # If the net margin or prestation margin is negative
            if com_params['m_mn'] < float(0) or com_params['p_m'] < float(0):
                salesmen_dict[salesman.id] = False
                continue

            commission = formula.format(**com_params)
            commission = eval(commission)*ratio
            salesman_dict['commission'] = commission
            salesmen_dict[salesman.id] = salesman_dict
            self.compvalues_data.set(
                key='prestation:salesman:{}'.format(salesman.id),
                target_id=presta.id,
                value=commission)

        return salesmen_dict

    def month_salesmen(self, compute=False, **kwargs):
        """Compute and return a dict indexed by the salesman.id of the salesmen
        of the month.

        Not optimized yet (not the same process than previous computation)

        Keyword arguments:
        month -- SQLA-Prestation (*)
        month_id -- id of the prestation (*)
        compute -- wether to compute missing data or not

        * at least one is required

        """
        month = self._get_month(**kwargs)
        salesmen_dict = {}

        Salesman = self.Salesman.Salesman
        Prestation = self.Prestation.Prestation
        salesmen = self.session.query(Salesman).all()

        for salesman in salesmen:

            salesmen_dict[salesman.id] = {}
            salesmen_dict[salesman.id]['commission'] = float(0)

            comp_value = self._get_computed_value(
                key='month:salesman:{}'.format(salesman.id),
                target_id=month.id)

            if comp_value is not None:
                salesmen_dict[salesman.id]['commission'] = comp_value.value
                continue

            prestations = self.session.query(Prestation)\
                .join(Prestation.salesmen)\
                .filter(Salesman.id == salesman.id)\
                .filter(Prestation.date >= month.date)\
                .filter(Prestation.date < month.next_month())\
                .all()

            for presta in prestations:
                comp_value = self._get_computed_value(
                    key='prestation:salesman:{}'.format(salesman.id),
                    target_id=presta.id)

                if not comp_value and not compute:
                    salesmen_dict[salesman.id] = False
                    continue

                if not salesmen_dict[salesman.id]:
                    continue

                if comp_value:
                    salesmen_dict[salesman.id]['commission'] += comp_value.value
                    continue

                presta_sm = self.prestation_salesmen(
                    compute=True,
                    prestation=presta)

                if not presta_sm[salesman.id]:
                    continue

                salesmen_dict[salesman.id]['commission'] += presta_sm[salesman.id]['commission']

            if salesmen_dict[salesman.id]:
                self.compvalues_data.set(
                    key='month:salesman:{}'.format(salesman.id),
                    target_id=month.id,
                    value=salesmen_dict[salesman.id]['commission'])

        return salesmen_dict
