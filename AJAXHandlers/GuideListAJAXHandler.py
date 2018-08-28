from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Faculty, Batch
from django.http import JsonResponse
from django.core import serializers


class GuideListAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        guide_list = list(Faculty.objects.filter(is_guide=1).order_by('short_name'))
        flag = 1
        students_count = sum((x.strength for x in Batch.objects.all()))
        recommended_count = students_count / len(guide_list)
        if guide_list == []:
            flag = 0
            guide_list = list(Faculty.objects.all().order_by('short_name'))
        return JsonResponse({'result': serializers.serialize('python', guide_list), 'flag': flag, 'rc': int(recommended_count)})
