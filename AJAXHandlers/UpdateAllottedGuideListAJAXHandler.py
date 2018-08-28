import json

from AJAXHandlers.IAJAXHandler import IAJAXHandler
from django.http import JsonResponse
from django.core import serializers
from VivaManagementSystem.models import GuideStudentMap, Faculty, Student, Tutor
from VivaManagementSystem.models import VMS_Session

class UpdateAllottedGuideListAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        map_dict_string = http_request.POST.get("map_data")
        map_dict = json.loads(map_dict_string)


        map_dict_additional = list(GuideStudentMap.objects.filter(guide=Faculty.objects.get(employee_id=map_dict["guide"]))\
            .exclude(tutor=Tutor.objects.get(faculty_id=map_dict['tutor'])))
        map_record = GuideStudentMap(session=VMS_Session.objects.get(is_current=1),
                                     guide=Faculty.objects.get(employee_id=map_dict["guide"]),
                                     student=Student.objects.get(roll_no=map_dict['student']),
                                     tutor=Tutor.objects.get(faculty_id=map_dict['tutor']))
        map_record.save()
        if not map_dict_additional :
            return JsonResponse({'result': 'no_data'})

        return JsonResponse({'result':  serializers.serialize('json',map_dict_additional)})
