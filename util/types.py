"""
File that contains all the different Types used in the System
"""
from enum import Enum
import json

def for_django(cls):
    """
    Decorator that is to be used with Enums to give it access in templates
    """
    cls.do_not_call_in_templates = True
    return cls

@for_django
class UserRoles(Enum):
    """
    Various Roles played by the Faculty in the system
    """
    Admin = 'Administrator'
    VivaCoordinator = 'Viva Coordinator'
    Tutor = 'Tutor'
    Guide = 'Guide'
    Guest = 'Guest' # This is for default users who are not logged in.

    @staticmethod
    def get_type_from_str(str_value):
        '''
        Returns the UserRole based on the string value.
        '''
        for role in UserRoles:
            if role.value == str_value:
                return role
        return UserRoles.Guest

class ReportSubmissionStatus(Enum):
    '''
    Various states in the report submission process
    '''
    Submitted = 'Submitted'
    Pending = 'Pending'

class OperationStatus():
    """Class that holds the result of the operation along with the data payload
    """
    def __init__(self):
        """Constructor that sets the data initially
        """
        self.status = False
        self.message = ''
        self.payload = None

    def set_data(self, status, message, payload):
        """Method that sets the parameters

        :param status: a :Boolean: denoting the status of the operation.

        :param message: a :String: denoting the message based on the status

        :param payload: a :Object: of any JSON serializable class
        """
        self.status = status
        self.message = message
        self.payload = payload

    def to_json_string(self):
        """Encodes the object into JSON format as a string.

        :return: a :string: Object containing the JSON form of the OperationStatus Object
        """
        return json.dumps({
            'status': self.status,
            'message': self.message,
            'payload': self.payload
        })
