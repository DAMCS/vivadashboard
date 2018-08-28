"""
Module that contains common utils for the various models in the sytem
"""
from VivaManagementSystem.models import VMS_Session, Student, User
from django.core.exceptions import MultipleObjectsReturned

class ModelUtils:
    '''
    Container class for all the Utils
    '''
    @staticmethod
    def get_current_session():
        '''
        Gets the session with the is_current flag set to 1.
        Returns: VMS_Session | None
            VMS_Session object if only 1 row has the is_current flag.
            None otherwise.
        '''
        try:
            current_session = VMS_Session.objects.get(is_current=1)
        except MultipleObjectsReturned:
            print("Multiple records have is_current flag set in VMS_Session table.")
            return None
        return current_session
    
    @staticmethod
    def get_current_session_students():
        '''
        Method that returns all Students studying in the current Session.

        :return: List of Student Records
        '''
        current_session = ModelUtils.get_current_session()
        if current_session is None:
            return []
        return Student.objects.filter(session=current_session)

    @staticmethod
    def create_credentials_for_faculty(faculty, faculty_role):
        """Creates a User credential for the faculty with the given role.
        Arguments
        faculty_id - ID of the Faculty to target
        faculty_role - Role played in the systems

        :return: Boolean status of the creation process
        """
        # Create a password from the faculty Object
        new_password = faculty.employee_id.upper
        new_credentials = User(
            user=faculty,
            user_pass=new_password,
            user_role=faculty_role
        )
        new_credentials.save()
        return True
