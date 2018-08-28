"""
Method for handling the AJAX Login requests
"""
import json
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from util.geolocation.geolocation import GeoLocationAPI
from VivaManagementSystem.models import Student
from util import SessionHandler, UserRoles
from util.ModelUtils import ModelUtils

class StudentLocationGraphAJAXHandler(IAJAXHandler):
    '''
    Invoked from the index page.
    Returns the dict of the various Locations and count of people in those locations
    '''
    def __init__(self):
        self.curr_session = None

    def handle_request(self, http_request):
        self.curr_session = ModelUtils.get_current_session()
        if self.curr_session is None:
            return json.dumps({'status' : False,
                               'msg': 'No active session. Set active session and try again.'})
        location_dict = dict()
        student_list = []
        for student in self.get_filtered_students():
            if student.address_city == '':
                try:
                    student.address_city = GeoLocationAPI(student.address_short_url) \
                                                .get_city_from_location()
                except Exception:
                    student.address_city = 'Others'
                student.save()
            if student.address_city in location_dict:
                location_dict[student.address_city] += 1
            else:
                location_dict[student.address_city] = 1
        # Format the list according to Morris Chart format
        return_data = []
        for location in location_dict.keys():
            location_entry = dict()
            location_entry['label'] = location
            location_entry['value'] = location_dict[location]
            return_data.append(location_entry)
        return json.dumps(return_data)

    def get_filtered_students(self):
        '''
        Returns a list of students to display according to the user requesting the data
        Admin / VivaCoordinator - All students list
        Tutor - Respective students in particular course for which faculty is a tutor for.
        '''
        curr_user_role = SessionHandler.get_user_role()
        if curr_user_role == UserRoles.Admin or curr_user_role == UserRoles.VivaCoordinator:
            return Student.objects.filter(session=self.curr_session)
        elif curr_user_role == UserRoles.Tutor:
            tutor_for_course = SessionHandler.get_user_course_id()
            return Student.objects.filter(
                session=self.curr_session,
                course=tutor_for_course
            )
        return []
