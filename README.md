TODO:

* Update model checker
* Add test to check expirations with different cache systems
* Manage Salesman removal
* Create a fonction to monkey patch other business objects
    eg: def patch_bo(bo):
            setattr(bo.get, 'prestations', PrestationRepository)