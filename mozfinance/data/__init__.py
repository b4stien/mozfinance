# -*- coding: utf-8 -*-
"""Package for all object API."""
from dogpile.cache.api import NoValue

from mozbase.data import InnerBoDataRepository


class DataRepository(InnerBoDataRepository):
    """ABC for data repository objects.

    Provide (mainly):
        - Get worker
        - Expire worker

    But also:
        - user (in self._user)
        - package (in self._package)

    """

    def __init__(self, bo=None, package=None):
        """Init a DataRepository object.

        Arguments:
            dbsession -- SQLA-Session, with cache region in dbsession.cache
            package -- package holding the models

        Keyword arguments:
            user -- user using the DataRepository
            user_id -- id of the user

        """
        InnerBoDataRepository.__init__(self, bo)

        if not package:
            raise TypeError('package not provided')

        self._package = package

    def _expire_instance(self, instance, ksk_tpl_name=None):
        """Expire every key related to an instance by deleting every key
        stored in its key_store.

        Argument:
            ksk_tpl_name -- default: _key_store_key_template
                            name of the attribute in which is saved the
                            template of the key store's key.

        """
        format_dict = dict()
        format_dict['instance'] = instance

        if ksk_tpl_name is None:
            ksk_tpl_name = '_key_store_key_template'

        key_store_key = getattr(instance, ksk_tpl_name).format(**format_dict)

        key_store = self._dbsession.cache.get(key_store_key)
        if isinstance(key_store, NoValue):
            key_store = []

        for key in key_store:
            self._dbsession.cache.delete(key)
