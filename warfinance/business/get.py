from . import AbcBusinessWorker
from compute import ComputeWorker


class GetWorker(AbcBusinessWorker):
    """BusinessWorker to get SQLA-objects with additional datas."""

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.compute = ComputeWorker(**kwargs)

    def _add_attributes(self, instance_type, instance, compute):

        # dict of all the possible additional attributes
        attr_dict = self._attributes_dict[instance_type]

        for key in attr_dict:
            comp_value = self._get_computed_value(
                key=instance_type+':'+key,
                target_id=instance.id)

            # The value of the additional attribute is in DB.
            if comp_value is not None:
                setattr(instance, key, comp_value.value)

            # The value is not in DB but "compute" is True
            elif compute:
                kwargs = {instance_type: instance}
                comp_value = getattr(self.compute, attr_dict[key])(**kwargs)
                setattr(instance, key, comp_value)

            # The value cannot be set
            else:
                setattr(instance, key, None)

        return instance

    def month(self, compute=False, **kwargs):
        """Return a month with additional attributes.

        Keyword arguments:
        month -- see warfinance.data.DataRepository._get_month (*)
        month_id -- see warfinance.data.DataRepository._get_month (*)
        date -- see warfinance.data.DataRepository._get_month (*)
        compute -- (bool) Wether to compute missing attributes or not.

        * at least one is required

        """
        month = self._get_month(**kwargs)

        month = self._add_attributes('month', month, compute)

        return month
