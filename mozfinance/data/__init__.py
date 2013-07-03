# -*- coding: utf-8 -*-
"""Package for all object API."""
from mozbase.data import RawDataRepository

from mozfinance.data.subworkers.get import GetWorker
from mozfinance.data.subworkers.expire import ExpireWorker


class DataRepository(RawDataRepository):
    """ABC for data repository objects.

    Provide (mainly):
        - Get worker
        - Expire worker

    But also:
        - user (in self._user)
        - package (in self._package)

    """

    def __init__(self, dbsession=None, package=None):
        """Init a DataRepository object.

        Arguments:
            dbsession -- SQLA-Session, with cache region in dbsession.cache
            package -- package holding the models

        Keyword arguments:
            user -- user using the DataRepository
            user_id -- id of the user

        """
        RawDataRepository.__init__(self, dbsession)

        if not package:
            raise TypeError('package not provided')

        self._package = package

        self._get = GetWorker(dbsession=dbsession, package=package)
        self._expire = ExpireWorker(dbsession=dbsession, package=package)
