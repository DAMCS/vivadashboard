from django.http import JsonResponse

from AJAXHandlers.IAJAXHandler import IAJAXHandler
from util import GenericUtil
from util import spreadsheet_module


class SyncDataAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        if GenericUtil.is_connected():
            spreadsheet_module.update_database(None)

        return JsonResponse({'result': 'success'})
