from importlib import import_module

from warbdata.actions import ActionsData

from . import DataRepository


class PrestationsData(DataRepository):
    """DataRepository object for costs."""

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
            raise TypeError('Prestation informations (prestation or \
                             prestation_id) not provided')

    def set_selling_price(self, pop_action=False, **kwargs):
        """Set the price of a prestation. Return False if there is no update or
        the updated prestation otherwise.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        prestation_id -- id of the prestation to update (*)
        prestation -- prestation to update (*)
        selling_price -- new selling_price of the prestation (**)

        * at least one is required
        ** see warbmodel.Prestation.PrestationSchema for expected types

        """
        presta = self._get_prestation(**kwargs)

        if not 'selling_price' in kwargs:
            raise TypeError('selling_price missing')

        if not isinstance(float, kwargs['selling_price']):
            raise AttributeError('selling_price isn\'t a float')

        if presta.selling_price == kwargs['selling_price']:
            return False

        presta.selling_price = kwargs['selling_price']

        self.session.flush()

        if pop_action:
            msg = self.Prestation.ACT_PRESTATION_SET_SELLING_PRICE
            self.actions_data.create(message=msg.format(presta.id))

        return presta
