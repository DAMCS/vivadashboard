"""
Method for handling the AJAX Login requests
"""
import json
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import User, Tutor
from util.SessionHandler import SessionHandler

class LoginAJAXHandler(IAJAXHandler):
    '''
    AJAXHandler for dealing with the login process.
    '''

    def handle_request(self, http_request):
        """
        Gets the username and password from the Request and then validates them from the DB
        :param http_request:
        :return: JSON response with the valid flag
        """
        # Make the userid case insensitive
        userid = http_request.POST['userid']
        password = http_request.POST['password']
        result = dict()
        result['status'] = 'fail'
        if SessionHandler.is_user_logged_in():
            result['msg'] = 'User already logged in. Logout and try again.'
            return json.dumps(result)
        try:
            # TODO Changing this to case insensitive is causing issues everywhere else. Enfore all caps user names
            user_obj = User.objects.get(user=userid, user_pass=password)
            tutor = Tutor.objects.select_related('faculty').filter(faculty=userid)
            # This is causing a error since the logged in faculty could also be an
            # Admin who is not a tutor for any course
            course_id = None
            if len(tutor) > 0:
                course_id = tutor[0].course.course_id
            user_obj.course_id = course_id # Used for creating the session.
            SessionHandler.login_user(user_obj)
            result['course_id'] = course_id
            result['status'] = 'success'
            result['role'] = user_obj.user_role
        except User.DoesNotExist:
            # Invalid user. Return error message
            result['msg'] = 'Invalid credentials.'
        # JSON Encode the results and send it back
        return json.dumps(result)
