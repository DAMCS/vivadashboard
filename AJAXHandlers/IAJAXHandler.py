"""
Interface used for all AJAX Calls
"""
from abc import ABCMeta, abstractmethod

class IAJAXHandler(metaclass=ABCMeta):
    """
    All AJAX Handling code shound be defined using this as base class.
    """
    @abstractmethod
    def handle_request(self, http_request):
        """
        Handles the request for the particular AJAX Call

        :param http_request: Request object from the Views module.

        :return: a :class: ResponseObject containing the result of the data
        """
        pass
