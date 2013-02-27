from importlib import import_module

from . import DataRepository


class PrestationsData(DataRepository):
    """DataRepository object for prestations."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Prestation = import_module('.Prestation', package=self.package)

    def _get_prestation(self, **kwargs):
        """Return a prestation given a prestation (other SQLA-Session) or a
        prestation_id."""
        if 'prestation' in kwargs:
            if not isinstance(kwargs['prestation'],
                              self.Prestation.Prestation):
                raise AttributeError(
                    'prestation provided is not a wb-Prestation')

            # Merging prestation which may come from another session
            return self.session.merge(kwargs['prestation'])

        elif 'prestation_id' in kwargs:
            presta_id = kwargs['prestation_id']
            return self.session.query(self.Prestation.Prestation)\
                .filter(self.Prestation.Prestation.id == presta_id)\
                .one()

        else:
            raise TypeError(
                'Prestation informations (prestation or prestation_id) not provided')

    def add_salesman(self, pop_action=False, **kwargs):
        """Add a salesman to a prestation. Return an exception if this salesman
        is already associated with the prestation.

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
            # It may be useful to have a custom Exception
            raise Exception

        presta.salesmen.append(salesman)

        self.session.flush()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_ADD_SALESMAN
            self.actions_data.create(message=msg.format(presta.id))

        return presta

    def remove_salesman(self, pop_action=False, **kwargs):
        """Remove a salesman from a prestation. Return an exception if this
        salesman wasn't associated with the prestation.

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
            # Maybe it should be useful to have a custom Exception
            raise Exception

        presta.salesmen.remove(salesman)

        self.session.flush()

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

        self.session.flush()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_SELLING_PRICE
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

        self.session.flush()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_CUSTOM_COM_FORMULAE
            self.actions_data.create(message=msg.format(presta.id))

        return presta
