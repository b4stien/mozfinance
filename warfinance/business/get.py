from . import AbcBusinessWorker
from compute import ComputeWorker


class GetWorker(AbcBusinessWorker):

    def __init__(self, **kwargs):
        AbcBusinessWorker.__init__(self, **kwargs)
        self.compute = ComputeWorker(**kwargs)

    def _add_attributes(self, instance_type, instance, compute):
        attr_dict = self._attributes_dict[instance_type]
        for key in attr_dict:
            comp_value = self._get_computed_value(
                key=instance_type+':'+key,
                target_id=instance.id)
            if comp_value is not None:
                setattr(instance, key, comp_value.value)
            elif compute:
                kwargs = {instance_type: instance}
                comp_value = getattr(self.compute, attr_dict[key])(**kwargs)
                setattr(instance, key, comp_value)
            else:
                setattr(instance, key, None)

        return instance

    def month(self, compute=False, **kwargs):
        month = self._get_month(**kwargs)

        month = self._add_attributes('month', month, compute)

        return month
