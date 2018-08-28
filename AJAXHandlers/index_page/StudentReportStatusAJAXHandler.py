'''
Object for getting the result of the Student report submission status
'''
from VivaManagementSystem.models import Student
import json
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from util import ReportSubmissionStatus, SessionHandler, UserRoles, OperationStatus
from util.ModelUtils import ModelUtils

class StudentReportStatusAJAXHandler(IAJAXHandler):
    '''
    AJAX handler object to handle the request
    '''
    def __init__(self):
        self.curr_session = None

    def handle_request(self, http_request):
        """Returns a list of details regarding the submission status and viva allotment.

        :return: a :list: of status and count as payload.
        """
        status_counts = {
            ReportSubmissionStatus.Submitted.value: 0,
            ReportSubmissionStatus.Pending.value: 0
        }
        op_status = OperationStatus()
        # Set the current session
        self.curr_session = ModelUtils.get_current_session()
        if self.curr_session is None:
            op_status.set_data(False,
                               "Active session not set. Please set active session and continue.",
                               None)
            return op_status.to_json_string()
        # Segregate the data
        for student in self.get_filtered_students():
            status_counts[student.report_submission_status] += 1
        # Convert to a list and send
        return_data = [
            {
                'label': ReportSubmissionStatus.Submitted.value,
                'value': status_counts[ReportSubmissionStatus.Submitted.value]
            },
            {
                'label': ReportSubmissionStatus.Pending.value,
                'value': status_counts[ReportSubmissionStatus.Pending.value]
            }
        ]
        op_status.set_data(True, "", return_data)
        return op_status.to_json_string()

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
