"""This module provides a useful wrapper for all business objects in 
warfinance.business

"""
from business import get, compute, data


class BusinessWorker():
    """warfinance entry point. Provides all API."""

    def __init__(self, **kwargs):
    	self.get = get.GetWorker(**kwargs)
    	self.data = data.DataWorker(**kwargs)
    	self._compute = compute.ComputeWorker(**kwargs)