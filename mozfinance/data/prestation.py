# -*- coding: utf-8 -*-
from importlib import import_module

from mozbase.util.database import db_method

from mozfinance.data import cost
from . import DataRepository


class PrestationData(DataRepository):
    """DataRepository object for prestations."""

    _patch_exports = ['set_selling_price', 'add_salesman', 'remove_salesman',
                      'set_salesman_ratio', 'set_salesman_formula', 'cost']

    def __init__(self, bo=None):
        DataRepository.__init__(self, bo)
        self.Prestation = import_module('.Prestation', package=self._package)
        self.PrestationSalesman = import_module('.AssPrestationSalesman', package=self._package)

        self.cost = cost.CostPrestationData(self._bo)
        self.salesman = PrestationSalesmanData(self._bo)
        self.bill = BillPrestationData(self._bo)

    def _get(self, prestation_id=None, prestation=None):
        """Return a prestation.

        Arguments:
            prestation -- explicit (*)
            prestation_id -- id of the prestation (*)

        * at least one is required

        """
        if prestation:
            if not isinstance(prestation, self.Prestation.Prestation):
                raise AttributeError(
                    'prestation provided is not a wb-Prestation')

            return prestation

        elif prestation_id:
            return self._dbsession.query(self.Prestation.Prestation)\
                .filter(self.Prestation.Prestation.id == prestation_id).one()

        else:
            raise TypeError(
                'Prestation informations (prestation or prestation_id) not provided')

    def get(self, prestation_id=None, prestation=None, **kwargs):
        """Return a prestation. Accept extra arguments."""
        return self._get(prestation_id, prestation)

    def _expire(self, prestation_id=None, prestation=None):
        """Expire a prestation and everything behind in the dependencies."""
        presta = self._get(prestation_id, prestation)
        self._expire_instance(presta)
        self._bo.month._expire(month=presta.month)


class BillPrestationData(DataRepository):

    def __init__(self, bo=None):
        DataRepository.__init__(self, bo)
        self.BillPrestation = import_module(
            '.BillPrestation',
            package=self._package)

    def _get(self, bill_id=None, bill=None):
        """Return a bill (BillPrestation).

        Keyword arguments:
            bill -- explicit (*)
            bill_id -- id of the bill (*)

        * at least one is required

        """
        if bill:
            if not isinstance(bill, self.BillPrestation.BillPrestation):
                raise AttributeError(
                    'bill provided is not a wb-BillPrestation')

            return bill

        elif bill_id:
            return self._dbsession.query(self.BillPrestation.BillPrestation)\
                .filter(self.BillPrestation.BillPrestation.id == bill_id).one()

        else:
            raise TypeError('Bill informations (bill or bill_id) not provided')

    def get(self, bill_id=None, bill=None, **kwargs):
        """Return a bill (BillPrestation). Accept extra arguments."""
        return self._get(bill_id, bill)

    @db_method
    def create(self, prestation_id=None, prestation=None, **kwargs):
        """Create a bill, add it to a prestation and return this bill.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            see mozfinance.data.BillPrestation.BillPrestationSchema

        * at least one is required

        """
        presta = self._bo.prestation._get(prestation_id, prestation)
        kwargs['prestation'] = presta

        self.BillPrestation.BillPrestationCreateSchema(kwargs)

        bill = self.BillPrestation.BillPrestation(**kwargs)
        self._dbsession.add(bill)

        self._bo.prestation._expire(prestation=presta)

        return bill

    @db_method
    def update(self, bill_id=None, bill=None, **kwargs):
        bill = self._get(bill_id, bill)
        update = self._update(
            instance=bill,
            schema=self.BillPrestation.BillPrestationUpdateSchema,
            **kwargs)
        self._bo.prestation._expire(prestation=bill.prestation)
        return update

    @db_method
    def remove(self, bill_id=None, bill=None):
        """Remove a bill, expire its prestation.

        Keyword arguments:
            bill_id -- id of the bill (*)
            bill -- bill (*)

        * at least one is required

        """
        bill = self._get(bill_id, bill)

        self._bo.prestation._expire(prestation=bill.prestation)
        self._dbsession.delete(bill)


class PrestationSalesmanData(DataRepository):

    def __init__(self, bo=None):
        DataRepository.__init__(self, bo)
        self.PrestationSalesman = import_module(
            '.AssPrestationSalesman',
            package=self._package)

    def _get(self, prestation_id=None, prestation=None,
            salesman_id=None, salesman=None):
        """Get and return a PrestationSalesman object. Will raise an
        exception if no result is found.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._bo.prestation._get(prestation_id, prestation)
        salesman = self._bo.salesman._get(salesman_id, salesman)

        presta_sm = presta.prestation_salesmen_query\
            .filter(self.PrestationSalesman.PrestationSalesman.salesman == salesman)\
            .one()

        return presta_sm

    def get(self, prestation_id=None, prestation=None,
            salesman_id=None, salesman=None, **kwargs):
        """Return a PrestationSalesman association. Accept extra
        arguments.

        """
        return self._get(prestation_id, prestation, salesman_id, salesman)

    def _expire(self, prestation_id=None, prestation=None):
        """Expire every prestation-salesman association of the given
        prestation, and every month-salesman association of the given
        prestation's month.

        Also expire the commission's key store of the prestation and the
        one of the prestation's month.

        """
        presta = self._bo.prestation._get(prestation_id, prestation)

        for presta_sm in presta.prestation_salesmen:
            self._expire_instance(presta_sm)

        self._expire_instance(presta, '_com_ksk_template')
        self._expire_instance(presta.month, '_com_ksk_template')

        self._bo.month.salesman._expire(month=presta.month)

    @db_method
    def add(self, prestation_id=None, prestation=None, salesman_id=None,
            salesman=None):
        """Add a salesman to a prestation and return True. If this salesman is
        already associated with the prestation, return False.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._bo.prestation._get(prestation_id, prestation)
        salesman = self._bo.salesman._get(salesman_id, salesman)

        if salesman in presta.salesmen:
            return False

        presta_sm = self.PrestationSalesman.PrestationSalesman()
        presta_sm.prestation = presta
        presta_sm.salesman = salesman
        presta_sm.formula = salesman.commissions_formulae[presta.sector][presta.category]

        self._dbsession.add(presta_sm)

        self._expire(prestation=presta)

        return True

    @db_method
    def remove(self, prestation_id=None, prestation=None, salesman_id=None,
        salesman=None):
        """Remove a salesman from a prestation. If this salesman wasn't
        associated with the prestation, do nothing.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)

        * at least one is required
        ** at least one is required

        """
        presta = self._bo.prestation._get(prestation_id, prestation)
        salesman = self._bo.salesman._get(salesman_id, salesman)

        if not salesman in presta.salesmen:
            return presta

        # We have to get the correct PrestationSalesman object.
        presta_sm = self._get(
            prestation=presta,
            salesman=salesman)

        self._dbsession.delete(presta_sm)

        self._expire(prestation=presta)

        return presta

    @db_method
    def set_ratio(self, prestation_id=None, prestation=None, salesman_id=None,
            salesman=None, ratio=None):
        """Set a custom ratio for a specific salesman/prestation. Return False
        if there is no update or True otherwise.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)
            ratio -- the ratio to set (or None)

        * at least one is required
        ** at least one is required

        """
        presta = self._bo.prestation._get(prestation_id, prestation)

        if not isinstance(ratio, float) and not ratio is None:
            raise AttributeError('ratio isn\'t a float and isn\'t None')

        presta_sm = self._get(prestation=presta,
            salesman_id=salesman_id,
            salesman=salesman)

        if presta_sm.ratio == ratio:
            return False

        presta_sm.ratio = ratio

        self._expire(prestation=presta)

        return True

    @db_method
    def set_formula(self, prestation_id=None, prestation=None, salesman_id=None,
            salesman=None, formula=None):
        """Set a custom commission formula for a specific salesman/prestation.
        Return False if there is no update or True otherwise.

        If no formula is given, we use the default salesman's formula.

        Keyword arguments:
            prestation_id -- id of the prestation (*)
            prestation -- prestation (*)
            salesman_id -- salesman (**)
            salesman -- id of the salesman (**)
            formula -- the formula to set (or None)

        * at least one is required
        ** at least one is required

        """
        presta = self._bo.prestation._get(prestation_id, prestation)
        salesman = self._bo.salesman._get(salesman_id, salesman)

        if not isinstance(formula, str) and not formula is None:
            raise AttributeError('formula isn\'t a string and isn\'t None')

        presta_sm = self._get(prestation=presta, salesman=salesman)

        if presta_sm.formula == formula:
            return False

        if formula is None:
            presta_sm.formula = salesman.commissions_formulae[presta.category][presta.sector]
        else:
            presta_sm.formula = formula

        self._expire(prestation=presta)

        return presta
