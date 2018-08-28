"""
Handler for getting details of the Students Alloted for a particular Guide
"""
# Imports
import json
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from util import SessionHandler
from util.ModelUtils import ModelUtils
from VivaManagementSystem.models import GuideStudentMap

class AllotedStudentDetailsAH(IAJAXHandler):
    '''
    Class for handling the AJAX Request for the Student Alloted Details
    '''
    def handle_request(self, http_request):
        # Get the alloted students for the particular guide.
        curr_user_id = SessionHandler.get_user_id()
        curr_session_id = ModelUtils.get_current_session()
        if curr_session_id is None:
            return json.dumps(
                {'status': False, 'error': 'Current session is not defined. Contact Administrator'})
        # Get the students alloted for the current active session.
        alloted_students = GuideStudentMap.objects.filter(
            session_id=curr_session_id.session_id,
            guide_id=curr_user_id
        )
        if len(alloted_students):
            print(alloted_students)
            return json.dumps({
                'status': True,
                'data': self.prepare_alloted_student_list(alloted_students)
            })
        else:
            return json.dumps({'status': False, 'error': 'No students alloted yet.'})

    def prepare_alloted_student_list(self, alloted_students):
        '''
        Converts the given alloted_student list from QuerySet to a list
        '''
        alloted_student_list = []
        for student_map in alloted_students:
            alloted_student_list.append({
                'name': student_map.student.name,
                'roll_no': student_map.student.roll_no,
                'organization_name': student_map.student.organization_name
            })
        return alloted_student_list
