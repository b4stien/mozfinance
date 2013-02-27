from . import AbcBusinessWorker
from compute import ComputeWorker

ATTRIBUTES_DICT = {
    'month': [
        ('revenu', 'month_revenu'),
        ('gross_margin', 'month_gross_margin'),
        ('cost', 'month_cost')
    ]
}


class GetWorker(AbcBusinessWorker):

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.compute = ComputeWorker(**kwargs)

    def _add_attributes(self, instance_type, instance, compute):
        for (key, method) in ATTRIBUTES_DICT[instance_type]:
            value = self._get_computed_value(
                key=instance_type+':'+key,
                target_id=instance.id)
            if value is not None:
                setattr(instance, key, value)
            elif compute:
                kwargs = {instance_type: instance}
                comp_value = getattr(self.compute, method)(**kwargs)
                setattr(instance, key, comp_value)
            else:
                setattr(instance, key, None)

    def month(self, compute=False, **kwargs):
        month = self._get_month(**kwargs)

        month = self._add_attributes('month', month, compute)

        return month
