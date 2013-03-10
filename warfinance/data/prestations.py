from importlib import import_module

from . import DataRepository


class PrestationsData(DataRepository):
    """DataRepository object for prestations."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Prestation = import_module('.Prestation', package=self.package)

    def add_salesman(self, pop_action=False, **kwargs):
        """Add a salesman to a prestation. If this salesman is already
        associated with the prestation, do nothing.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation (*)
        prestation -- prestation (*)
        salesman_id -- salesman (**)
        salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._get_prestation(**kwargs)
        salesman = self._get_salesman(**kwargs)

        if salesman in presta.salesmen:
            return presta

        presta.salesmen.append(salesman)

        self.session.commit()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_ADD_SALESMAN
            self.actions_data.create(message=msg.format(presta.id))

        return presta

    def remove_salesman(self, pop_action=False, **kwargs):
        """Remove a salesman from a prestation. If this salesman wasn't
        associated with the prestation, do nothing.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation (*)
        prestation -- prestation (*)
        salesman_id -- salesman (**)
        salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._get_prestation(**kwargs)
        salesman = self._get_salesman(**kwargs)

        if not salesman in presta.salesmen:
            return presta

        presta.salesmen.remove(salesman)

        self.session.commit()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_REMOVE_SALESMAN
            self.actions_data.create(message=msg.format(presta.id))

        return presta

    def set_selling_price(self, pop_action=False, **kwargs):
        """Set the price of a prestation. Return False if there is no update or
        the updated prestation otherwise.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation to update (*)
        prestation -- prestation to update (*)
        selling_price -- new selling_price of the prestation (**)

        * at least one is required
        ** see warfinance.data.model.Prestation.PrestationSchema for expected types

        """
        presta = self._get_prestation(**kwargs)

        if not 'selling_price' in kwargs:
            raise TypeError('selling_price missing')

        if not isinstance(kwargs['selling_price'], float):
            raise AttributeError('selling_price isn\'t a float')

        if presta.selling_price == kwargs['selling_price']:
            return False

        presta.selling_price = kwargs['selling_price']

        self.session.commit()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_SELLING_PRICE
            self.actions_data.create(message=msg.format(presta.id))

        return presta

    def set_custom_ratios(self, pop_action=False, **kwargs):
        """Set a custom ratio for a specific salesman/prestation. Return False
        if there is no update or the updated prestation otherwise.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation (*)
        prestation -- prestation (*)
        salesman_id -- salesman (**)
        salesman -- id of the salesman (**)
        ratio -- the ratio to set

        * at least one is required
        ** at least one is required

        """
        presta = self._get_prestation(**kwargs)
        salesman = self._get_salesman(**kwargs)

        if not 'ratio' in kwargs:
            raise TypeError('ratio missing')

        if not isinstance(kwargs['ratio'], float):
            raise AttributeError('ratio isn\'t a float')

        custom_ratio = (salesman.id, kwargs['ratio'])

        if presta.custom_ratios is None:
            presta.custom_ratios = [custom_ratio]

        elif custom_ratio in presta.custom_ratios:
            return False

        for (sm_id, ratio) in presta.custom_ratios:
            if sm_id == salesman.id:
                presta.custom_ratios.remove((sm_id, ratio))

        presta.custom_ratios.append(custom_ratio)

        self.session.commit()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_CUSTOM_RATIOS
            self.actions_data.create(message=msg.format(presta.id))

        return presta

    def set_custom_com_formula(self, pop_action=False, **kwargs):
        """Set a custom commission formula for a specific salesman/prestation.
        Return False if there is no update or the updated prestation otherwise.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation (*)
        prestation -- prestation (*)
        salesman_id -- salesman (**)
        salesman -- id of the salesman (**)
        commission_formula -- the formula to set

        * at least one is required
        ** at least one is required

        """
        presta = self._get_prestation(**kwargs)
        salesman = self._get_salesman(**kwargs)

        if not 'commission_formula' in kwargs:
            raise TypeError('commission_formula missing')

        if not isinstance(kwargs['commission_formula'], str):
            raise AttributeError('commission_formula isn\'t a string')

        # We may test kwargs['commission_formula'] here ...

        custom_com_formula = (salesman.id, kwargs['commission_formula'])

        if presta.custom_com_formulae is None:
            presta.custom_com_formulae = [custom_com_formula]

        elif custom_com_formula in presta.custom_com_formulae:
            return False

        for (sm_id, com) in presta.custom_com_formulae:
            if sm_id == salesman.id:
                presta.custom_com_formulae.remove((sm_id, com))

        presta.custom_com_formulae.append(custom_com_formula)

        self.session.commit()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_CUSTOM_COM_FORMULAE
            self.actions_data.create(message=msg.format(presta.id))

        return presta
