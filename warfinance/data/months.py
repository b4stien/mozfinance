from importlib import import_module
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'fr_FR')

from . import DataRepository


class MonthsData(DataRepository):
    """DataRepository object for costs."""

    def __init__(self, **kwargs):
        DataRepository.__init__(self, **kwargs)
        self.Month = import_module('.Month', package=self.package)

    def create(self, **kwargs):
        """Create and insert a month in DB. Return this month.

        Keyword arguments:
        see warfinance.datamodel.Month.MonthSchema

        """
        cost_schema = self.Month.MonthSchema(kwargs)  # Validate datas

        month = self.Month.Month(**kwargs)
        self.session.add(month)

        # To get a full month to return (get a working id)
        self.session.flush()

        return month

    def update(self, pop_action=False, **kwargs):
        """Update a month. Return False if there is no update or the updated
        month.

        Keyword arguments:
        pop_action -- wether to pop an action or not
        month_id -- id of the month to update (*)
        month -- month to update (*)
        date -- date of the month to update (*) (!! it is not the "new" date of
            the month)
        breakeven -- new breakeven of the month (**)

        * at least one is required
        ** see warfinance.datamodel.Month.MonthSchema for expected type

        """
        month = self._get_month(**kwargs)

        month_dict = {k: v for k, v in month.__dict__.items()
                      if k in month.create_dict}
        new_month_dict = month_dict.copy()

        item_to_update = [item for item in month.update_dict if item in kwargs]

        for item in item_to_update:
            new_month_dict[item] = kwargs[item]

        self.Month.MonthSchema(new_month_dict)

        for item in item_to_update:
            month.__dict__[item] = kwargs[item]

        if new_month_dict == month_dict:
            return False

        self.session.flush()

        if pop_action:
            datetime_date = datetime.datetime.combine(
                month.date, datetime.time())
            date_name = datetime_date.strftime('%B %Y').decode('utf8')
            self.actions_data.create(
                message=self.Month.ACT_MONTH_UPDATE.format(date_name))

        return month

    def remove(self, **kwargs):
        """There is no point in removing a month from DB."""
        raise NotImplementedError
