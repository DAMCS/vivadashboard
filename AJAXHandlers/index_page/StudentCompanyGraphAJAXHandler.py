"""
Method for handling the AJAX Login requests
"""
import json
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Student
from util import SessionHandler, UserRoles
from util.ModelUtils import ModelUtils

class StudentCompanyGraphAJAXHandler(IAJAXHandler):
    '''
    Invoked from the index page.
    Returns the dict of the various Locations and count of people in those locations
    TODO Rename the class
    '''
    def __init__(self):
        '''
        Constructor for setting required attributes
        '''
        self.curr_session = None

    def handle_request(self, http_request):
        # Check the session data
        self.curr_session = ModelUtils.get_current_session()
        if self.curr_session is None:
            return json.dumps({
                'status' : False,
                'msg': 'No active session. Set active session and try again.'
            })
        company_names_dict = dict()
        for student in self.get_filtered_students():
            org_name_clean = student.organization_name.lower().strip()
            if org_name_clean in company_names_dict:
                company_names_dict[org_name_clean] += 1
            else:
                company_names_dict[org_name_clean] = 1
        # Format the list according to Morris Chart format
        return_data = []
        for company in sorted(company_names_dict.keys()):
            company_entry = dict()
            company_entry['name'] = company.title()
            company_entry['count'] = company_names_dict[company]
            return_data.append(company_entry)
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
