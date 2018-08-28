import json

from django.http import JsonResponse

from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Course
from django.core import serializers


class CourseListAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        course_list = list(Course.objects.all())
        course_list.sort(key=lambda x: x.course_name, reverse=False)
        return JsonResponse({'result': serializers.serialize('python', course_list)})
