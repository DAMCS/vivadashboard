import json

from AJAXHandlers.IAJAXHandler import IAJAXHandler
from django.http import JsonResponse
from django.core import serializers

from VivaManagementSystem.models import GuideStudentMap


class DeleteAllottedGuideListAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        data_string = http_request.POST.get("delete_input")
        data = json.loads(data_string)
        GuideStudentMap.objects.get(student=data["roll"],guide=data["emp_id"]).delete();
        return JsonResponse({'result':  'success'})