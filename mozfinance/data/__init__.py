# -*- coding: utf-8 -*-
"""Package for all object API."""
from mozbase.data import AuthenticatedDataRepository
from mozbase.data.action import ActionData
from mozbase.util.cache import Cache

from mozfinance.data.subworkers.get import GetWorker
from mozfinance.data.subworkers.expire import ExpireWorker
from mozfinance.data.subworkers.compute import ComputeWorker
import mozfinance


class DataRepository(AuthenticatedDataRepository):
    """ABC for data repository objects.

    Provide (mainly):
        - ActionData object
        - Cache interaction
        - Get worker
        - Expire worker
        - Compute worker

    But also:
        - user (in self._user)
        - package (in self._package)

    """

    def __init__(self, dbsession=None, package=None, cache=None, **kwargs):
        """Init a DataRepository object.

        Arguments:
            dbsession -- SQLA-Session
            package -- package holding the models
            cache -- cache interface

        Keyword arguments:
            user -- user using the DataRepository

        """
        AuthenticatedDataRepository.__init__(self, dbsession, **kwargs)

        if not package:
            raise TypeError('package not provided')

        self._package = package

        if not cache:
            self._cache = Cache()
        else:
            self._cache = cache

        self.action_data = ActionData(dbsession=dbsession, **kwargs)

        self._attributes_dict = mozfinance._ATTRIBUTES_DICT

        self._get = GetWorker(dbsession=dbsession, package=package)
        self._expire = ExpireWorker(
            dbsession=dbsession,
            package=package,
            cache=self._cache)
        self._compute = ComputeWorker(
            dbsession=dbsession,
            package=package,
            cache=self._cache)

    def _add_attributes(self, instance_type, instance, compute):
        """Return an augmented version of the given instance.

        Arguments:
            instance_type -- name of the given instance
            instance -- instance to augmente
            compute -- (bool) wether to compute missing datas or not

        """

        # dict of all the possible additional attributes
        attr_dict = self._attributes_dict[instance_type]

        for key in attr_dict:

            comp_value = self._cache.get(
                key='{}:{}:{}'.format(instance_type, instance.id, key))

            # The value of the additional attribute is in cache.
            if comp_value is not None:
                setattr(instance, key, comp_value)

            # The value is not in cache but "compute" is True
            elif compute:
                kwargs = {instance_type: instance}
                comp_value = getattr(self._compute, attr_dict[key])(**kwargs)
                setattr(instance, key, comp_value)

            # The value cannot be set
            else:
                setattr(instance, key, None)

        return instance
