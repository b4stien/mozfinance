mozfinance
==========

Dependencies
------------

* [mozbase](https://github.com/b4stien/mozbase) (0.3.x)
  * [SQLAlchemy](http://hg.sqlalchemy.org/sqlalchemy) (0.8.1)
  * [Voluptuous](https://github.com/alecthomas/voluptuous) (0.7.2)
  * [dogpile.cache](http://dogpilecache.readthedocs.org/en/latest/) (0.4.3)


To do
-----

* Add test to check expirations with different cache systems
* Manage Salesman removal
* Create a fonction to monkey patch other business objects
    eg: def patch_bo(bo):
            setattr(bo.get, 'prestations', PrestationRepository)
