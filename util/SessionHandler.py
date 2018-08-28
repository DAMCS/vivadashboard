"""
Handles all things related to the Sessions
"""
from enum import Enum
from datetime import datetime
from util.configuration import ConfigurationManager
from util.types import UserRoles


class SessionVariableKeys(Enum):
    """
    Stores the keys used in the session storage
    """
    USER_ID = 'user_id',
    USER_ROLE = 'user_role',
    USER_COURSE_ID = 'course_id'
    IS_LOGGED_IN = 'is_logged_in',
    LAST_ACTIVE = 'last_active'


class SessionHandler:
    """
    Handles all session related activites
    """
    # Variable that stores the session object of the current request
    __session_obj = None
    # Validity time for the session
    __SESSION_VALID_TIME = 60 * 30

    @staticmethod
    def set_session_obj(session_obj):
        """
        Method for setting the session object which is getting attached to the request.
        :param session_obj: Request's session obj
        :return: None
        """
        SessionHandler.__session_obj = session_obj
        # Now update the session
        SessionHandler.update_active_session()

    @staticmethod
    def login_user(user_obj):
        """
        Method for logging in the user by setting the required  session variables
        :param user_obj: Details about the authenticated user
        :return: None
        """
        SessionHandler.__set_session_var(SessionVariableKeys.IS_LOGGED_IN, True)
        SessionHandler.__set_session_var(SessionVariableKeys.LAST_ACTIVE, datetime.now())
        SessionHandler.__set_session_var(SessionVariableKeys.USER_ID, user_obj.user_id)
        SessionHandler.__set_session_var(SessionVariableKeys.USER_ROLE, user_obj.user_role)
        SessionHandler.__set_session_var(SessionVariableKeys.USER_COURSE_ID, user_obj.course_id)

    @staticmethod
    def is_user_logged_in():
        """
        Method for checking if the user is logged in or not
        :return: True if the user is logged in. False otherwise.
        """
        try:
            return SessionHandler.__get_session_var(SessionVariableKeys.IS_LOGGED_IN)
        except KeyError:
            return False

    @staticmethod
    def update_active_session():
        """
        Method for updating the current sessions's timestamp
        :return: None
        """
        ConfigurationManager.get_instance()
        if not SessionHandler.__session_obj.has_key(SessionVariableKeys.IS_LOGGED_IN):
            # Set them to the defaults and return
            SessionHandler.__set_session_var(SessionVariableKeys.IS_LOGGED_IN, False)
            SessionHandler.__set_session_var(SessionVariableKeys.LAST_ACTIVE, datetime.now())
            SessionHandler.__set_session_var(SessionVariableKeys.USER_ID, None)
            return
        if SessionHandler.__get_session_var(SessionVariableKeys.IS_LOGGED_IN):
            now_time = datetime.now()
            time_diff = now_time - SessionHandler.__get_session_var(SessionVariableKeys.LAST_ACTIVE)
            if time_diff.seconds > SessionHandler.__SESSION_VALID_TIME:
                # Invalidate the session since it has been inactive for too long.
                SessionHandler.__set_session_var(SessionVariableKeys.IS_LOGGED_IN, False)
        SessionHandler.__set_session_var(SessionVariableKeys.LAST_ACTIVE, datetime.now())

    @staticmethod
    def get_user_role():
        """
        Method for getting the type of the logged in user.
        :return: Type of the user logged in.
        """
        user_type_raw = SessionHandler.__get_session_var(SessionVariableKeys.USER_ROLE)
        for role in UserRoles:
            if user_type_raw == role.value:
                return role
        return UserRoles.Guest

    @staticmethod
    def get_user_id():
        """
        Returns the user_id from the stored session.
        :return: ID of the logged in user
        """
        return SessionHandler.__get_session_var(SessionVariableKeys.USER_ID)

    @staticmethod
    def get_user_course_id():
        """
        Returns the user_id from the stored session.
        :return: ID of the logged in user
        """
        return SessionHandler.__get_session_var(SessionVariableKeys.USER_COURSE_ID)


    @staticmethod
    def logout_user():
        """
        Method for destroying the session
        :return: None
        """
        SessionHandler.__set_session_var(SessionVariableKeys.IS_LOGGED_IN, False)
        SessionHandler.__set_session_var(SessionVariableKeys.USER_ID, None)

    @staticmethod
    def __get_session_var(var_key):
        """
        Method to get a session variable
        :param var_key: Variable key that is to be obtained from the Session
        :return: Value of the variable
        """
        try:
            return SessionHandler.__session_obj[var_key]
        except KeyError:
            return None

    @staticmethod
    def __set_session_var(var_key, var_value):
        """
        Sets the value of a particular session variable
        :param var_key: Variable to set
        :param var_value: Value of variable to set
        :return: None
        """
        SessionHandler.__session_obj[var_key] = var_value
