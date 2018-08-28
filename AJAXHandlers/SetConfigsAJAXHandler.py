from AJAXHandlers.IAJAXHandler import IAJAXHandler
from util.configuration.ConfigurationManager import ConfigurationManager
import json


class SetConfigsAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        """
        Sets the multiple configs that are sent.
        :param http_request:
        :return: string JSON reply
        """
        config_settings = json.loads(http_request.POST['configs'])
        config_manager = ConfigurationManager.get_instance()
        for config in config_settings:
            config_manager.set_config(config['config_key'], config['config_value'])
        return json.dumps({'status': 'success'})
