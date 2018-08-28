from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import VMS_Session
from util.configuration.ConfigurationManager import ConfigurationManager
import json


class ConfigPageOpenAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        """
        Returns the status of the various pages and the open status
        :param http_request: Request Data
        :return: Status of the various pages in the Config
        """
        ret_data = dict()
        """config_manager = ConfigurationManager.get_instance()"""
        page_data = []
        # Page 1 is always open
        page_data.append(True)
        # Page 2. Faculty selection. Requires Page one to be open.
        """if config_manager.get_config('Session_Year') is not None and config_manager.get_config('Session_Sem') is not None:
            page_data.append(True)
        else:
            page_data.append(False)"""
        session = VMS_Session.objects.filter(is_current=True)
        if session.count() > 0:
            page_data.append(True)
        else:
            page_data.append(False)
        # Page 3
        # TODO Check if all courses have been allotted with tutors

        ret_data['page_status'] = page_data
        return json.dumps(ret_data)