from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Course
from util.configuration.ConfigurationManager import ConfigurationManager
import json


class CourseModificationAJAXHandler(IAJAXHandler):
    """
    Handles everything related to adding and removing for courses.
    """
    def handle_request(self, http_request):
        """
        Does either remove or add operation for the Courses.
        :param http_request: Contains all the HTTP data
        :return: None
        """
        result = dict()
        result['status'] = 'fail'
        action = http_request.POST['action']
        course = http_request.POST['course']
        shortName = http_request.POST['shortName']
        degree = http_request.POST['degree']
        if action == 'add':
            newCourse = Course(course_name=course,short_name=shortName,degree_name=degree)
            newCourse.save()
        if action == 'remove':
            deleteCourse = Course.objects.filter(course_name=course)
            deleteCourse.delete()
        result['status'] = 'success'
        return json.dumps(result)

