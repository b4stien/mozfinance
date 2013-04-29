import datetime

from sqlalchemy.orm.exc import NoResultFound

from . import AbcBusinessWorker
from .. import COMMISSIONS_BONUS


class ComputeWorker(AbcBusinessWorker):
    """BusinessWorker for computation. All recipes to compute values are stored
    here."""

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.commissions_bonus = COMMISSIONS_BONUS

    def _get_or_compute(self, key, **kwargs):
        """Return a value (a real value and not a ComputedValue).

        Arguments:
        key -- key of the value (eg: "month:revenue").
               See warfinance.business.__ATTRIBUTES_DICT
        target_id -- id of the target

        Keyword arguments:
        instance -- target (SQLA-object)

        """
        # The "get" part of "get_or_compute"
        comp_value = self.cvalues_data.get(key=key)

        if comp_value:
            return comp_value

        # And the "compute" part
        split_key = key.split(':')
        if len(split_key) != 3:
            raise AttributeError('Incorrect key')
        method = self._attributes_dict[split_key[0]][split_key[2]]

        # To avoid useless DB call.
        if 'instance' in kwargs:
            method_kwargs = {split_key[0]: kwargs['instance']}
        else:
            method_kwargs = {split_key[0]+'_id': split_key[1]}

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
        self.cvalues_data.set(
            key='prestation:{}:cost'.format(presta.id),
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
            'prestation:{}:cost'.format(presta.id),
            instance=presta)

        if presta.selling_price:
            presta_margin = presta.selling_price - presta_cost
        else:
            presta_margin = float(0)

        # Storing value in DB
        self.cvalues_data.set(
            key='prestation:{}:margin'.format(presta.id),
            value=presta_margin)

        return presta_margin

    def month_revenue(self, **kwargs):
        """Compute and return the revenue of a month.

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

        month_revenue = float(0)
        for presta in prestations:
            if presta.selling_price is not None:
                month_revenue += presta.selling_price

        self.cvalues_data.set(
            key='month:{}:revenue'.format(month.id),
            value=month_revenue)

        return month_revenue

    def month_gross_margin(self, **kwargs):
        """Compute and return the gross margin of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenue

        """
        month = self._get_month(**kwargs)

        month_revenue = self._get_or_compute(
            'month:{}:revenue'.format(month.id),
            instance=month)
        month_cost = self._get_or_compute(
            'month:{}:total_cost'.format(month.id),
            instance=month)

        month_gross_margin = month_revenue - month_cost
        self.cvalues_data.set(
            key='month:{}:gross_margin'.format(month.id),
            value=month_gross_margin)

        return month_gross_margin

    def month_commission_base(self, **kwargs):
        """Compute and return the commission base of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenue

        """
        month = self._get_month(**kwargs)

        month_gross_margin = self._get_or_compute(
            'month:{}:gross_margin'.format(month.id),
            instance=month)

        month_commission_base = month_gross_margin
        if month.cost:
            month_commission_base -= month.cost
        if month.salaries:
            month_commission_base -= month.salaries

        self.cvalues_data.set(
            key='month:{}:commission_base'.format(month.id),
            value=month_commission_base)

        return month_commission_base

    def month_net_margin(self, **kwargs):
        """Compute and return the net margin of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenue

        """
        month = self._get_month(**kwargs)

        month_gross_margin = self._get_or_compute(
            'month:{}:gross_margin'.format(month.id),
            instance=month)

        month_net_margin = month_gross_margin
        if month.cost:
            month_net_margin -= month.cost
        if month.taxes:
            month_net_margin -= month.taxes
        if month.salaries:
            month_net_margin -= month.salaries
        if month.commissions_refined:
            month_net_margin -= month.commissions_refined

        self.cvalues_data.set(
            key='month:{}:net_margin'.format(month.id),
            value=month_net_margin)

        return month_net_margin

    def month_total_cost(self, **kwargs):
        """Compute and return the sum of the costs of the prestations of a month.

        Keyword arguments:
        same as warfinance.business.compute.ComputeWorker.month_revenue

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
                'prestation:{}:cost'.format(presta.id),
                instance=presta)

        self.cvalues_data.set(
            key='month:{}:total_cost'.format(month.id),
            value=month_cost)

        return month_cost

    def year_revenue(self, **kwargs):
        """Compute and return the cumulated revenue of the year

        Keyword arguments:
        date -- Date of the first day of the year
        year_id -- Fake id, year as an int"""

        year = self._get_year(**kwargs)

        now_date = datetime.datetime.now().date()

        revenue = float(0)

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

            month_revenue = self._get_or_compute(
                'month:{}:revenue'.format(m.id), instance=m)

            revenue += month_revenue

        self.cvalues_data.set(
            key='year:{}:revenue'.format(year.id),
            value=revenue)

        return revenue

    def year_gross_margin(self, **kwargs):
        """Compute and return the cumulated gross margin of the year

        Keyword arguments:
        date -- Date of the first day of the year
        year_id -- Fake id, year as an int"""

        year = self._get_year(**kwargs)

        now_date = datetime.datetime.now().date()

        gross_margin = float(0)

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

            month_gross_margin = self._get_or_compute(
                'month:{}:gross_margin'.format(m.id), instance=m)

            gross_margin += month_gross_margin

        self.cvalues_data.set(
            key='year:{}:gross_margin'.format(year.id),
            value=gross_margin)

        return gross_margin

    def year_net_margin(self, **kwargs):
        """Compute and return the cumulated net margin of the year

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
                'month:{}:net_margin'.format(m.id), instance=m)

            net_margin += month_net_margin

        self.cvalues_data.set(
            key='year:{}:net_margin'.format(year.id),
            value=net_margin)

        return net_margin

    def _get_prestation_commission_params(self, **kwargs):
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
            'm_ca': self._get_or_compute('month:{}:revenue'.format(m.id), instance=m),
            'm_mb': self._get_or_compute('month:{}:gross_margin'.format(m.id), instance=m),
            'm_bc': self._get_or_compute('month:{}:commission_base'.format(m.id), instance=m),
            'm_tc': self._get_or_compute('month:{}:total_cost'.format(m.id), instance=m),
            'm_ff': m.cost,
            'p_c': self._get_or_compute('prestation:{}:cost'.format(p.id), instance=p),
            'p_m': self._get_or_compute('prestation:{}:margin'.format(p.id), instance=p),
            'p_pv': p.selling_price,
        }
        for param in com_params:
            if not isinstance(com_params[param], float):
                return False
        return com_params

    def _get_month_commission_params(self, **kwargs):
        m = self._get_month(**kwargs)
        com_params = {
            'm_ca': self._get_or_compute('month:{}:revenue'.format(m.id), instance=m),
            'm_mb': self._get_or_compute('month:{}:gross_margin'.format(m.id), instance=m),
            'm_bc': self._get_or_compute('month:{}:commission_base'.format(m.id), instance=m),
            'm_tc': self._get_or_compute('month:{}:total_cost'.format(m.id), instance=m),
            'm_ff': m.cost,
        }
        for param in com_params:
            if not isinstance(com_params[param], float):
                return False
        return com_params

    def prestation_salesmen_com(self, compute=False, **kwargs):
        """Compute and return a dict indexed by the salesman.id of the salesmen
        of the prestation.

        Keyword arguments:
        prestation -- SQLA-Prestation (*)
        prestation_id -- id of the prestation (*)
        compute -- wether to compute missing data or not

        * at least one is required

        """
        presta = self._get_prestation(**kwargs)
        salesmen_dict = {}

        for presta_sm in presta.prestation_salesmen:

            if presta_sm.ratio:
                ratio = presta_sm.ratio
            else:
                ratio = float(1) / float(len(presta.salesmen))

            # Will eventualy change to keep history of formulae
            formula = presta_sm.formula
            salesman_dict = {
                'formula': formula,
                'ratio': ratio
            }

            # If we can't get all params
            com_params = self._get_prestation_commission_params(prestation=presta)
            if not com_params:
                salesman_dict['commission'] = False
                salesmen_dict[presta_sm.salesman.id] = salesman_dict
                continue

            # If the net margin or prestation margin is negative
            if com_params['m_bc'] < float(0) or com_params['p_m'] < float(0):
                salesman_dict['commission'] = False
                salesmen_dict[presta_sm.salesman.id] = salesman_dict
                continue

            commission = formula.format(**com_params)
            commission = round(eval(commission)*ratio, 1)
            salesman_dict['commission'] = commission
            salesmen_dict[presta_sm.salesman.id] = salesman_dict

        self.cvalues_data.set(
            key='prestation:{}:salesmen_com'.format(presta.id),
            value=salesmen_dict)

        return salesmen_dict

    def month_salesmen_com(self, compute=False, **kwargs):
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
        PrestationSalesman = self.PrestationSalesman.PrestationSalesman
        salesmen = self.session.query(Salesman).all()

        # Computing total_prestation
        for salesman in salesmen:

            salesmen_dict[salesman.id] = {}
            salesmen_dict[salesman.id]['total_prestations'] = float(0)
            salesmen_dict[salesman.id]['total_bonuses'] = float(0)
            salesmen_dict[salesman.id]['commission'] = float(0)

            # Computing prestations
            prestations = self.session.query(Prestation)\
                .join(Prestation.prestation_salesmen)\
                .filter(PrestationSalesman.salesman_id == salesman.id)\
                .filter(Prestation.date >= month.date)\
                .filter(Prestation.date < month.next_month())\
                .all()

            for presta in prestations:
                presta_sm = self._get_or_compute(
                    key='prestation:{}:salesmen_com'.format(presta.id),
                    instance=presta)

                if not presta_sm[salesman.id]['commission']:
                    continue

                salesmen_dict[salesman.id]['total_prestations'] += presta_sm[salesman.id]['commission']

            # Computing bonuses
            com_params = self._get_month_commission_params(month=month)
            if com_params:
                for bonus in self.commissions_bonus:
                    salesmen_dict[salesman.id]['total_bonuses'] += bonus(**com_params)

            # Rounding bonuses sum
            salesmen_dict[salesman.id]['total_bonuses'] = round(salesmen_dict[salesman.id]['total_bonuses'], 1)

            # Computing sum
            salesmen_dict[salesman.id]['commission'] += salesmen_dict[salesman.id]['total_prestations']
            salesmen_dict[salesman.id]['commission'] += salesmen_dict[salesman.id]['total_bonuses']

        self.cvalues_data.set(
            key='month:{}:salesmen_com'.format(month.id),
            value=salesmen_dict)

        return salesmen_dict
