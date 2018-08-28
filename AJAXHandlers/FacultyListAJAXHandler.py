import json
import math

from django.http import JsonResponse

from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Faculty, Batch
from django.core import serializers


class FacultyListAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        faculty_list = list(Faculty.objects.all().order_by('short_name'))
        # Find the count of the guides
        guides_count = sum(faculty.is_guide for faculty in faculty_list)
        if guides_count == 0:
            guides_count = 1
        # Get the total count
        students_count = sum((x.strength for x in Batch.objects.all()))
        return JsonResponse({
            'result': serializers.serialize('python', faculty_list),
            'rc':  math.ceil(students_count / guides_count)
        })
