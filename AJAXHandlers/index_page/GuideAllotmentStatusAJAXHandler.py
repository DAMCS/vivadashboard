"""
Method for handling the AJAX Login requests
"""
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from util import SessionHandler, UserRoles
from VivaManagementSystem.models import GuideStudentMap, VMS_Session

class GuideAllotmentStatusAJAXHandler(IAJAXHandler):
    '''
    Invoked from the index page.
    Returns the dict of the various Locations and count of people in those locations
    '''
    def handle_request(self, http_request):
        # Select the current session. is_active is true
        try:
            active_session = VMS_Session.objects.get(is_current=1)
        except MultipleObjectsReturned:
            # Too many current sessions.
            return JsonResponse({'status' : False, \
                                    'msg' : 'Multiple sessions marked is_current=1.\
                                             Only one active session allowed.'})
        # The current session should not be null either
        if active_session is None:
            return JsonResponse({'status': False, \
                                 'msg': 'No session marked with is_current=1'})
        # Get the details of the courses using active_session
        self.current_session = active_session
        return JsonResponse({
            'status': True,
            'data': self.get_guide_allot_status()
        })

    def get_guide_allot_status(self):
        '''
        Method to get the Count of alloted students for each Faculty.
        '''
        student_mappings = self.get_filtered_data()
        guide_count_mapping = dict()
        for mapping in student_mappings:
            guide_full_name = mapping.guide.name + '##' + mapping.guide.short_name
            if guide_full_name in guide_count_mapping:
                guide_count_mapping[guide_full_name] += 1
            else:
                guide_count_mapping[guide_full_name] = 1
        # Convert it to a better form for transmitting
        processed_data = []
        for faculty in guide_count_mapping:
            # Convert name to proper form
            name_parts = faculty.split('##')
            processed_data.append({
                'name': name_parts[0].strip(),
                'short_name': name_parts[1].strip(),
                'count': guide_count_mapping[faculty]
            })
        return processed_data

    def get_filtered_data(self):
        '''
        Filters the data according to the logged in user.
        '''
        user_role = SessionHandler.get_user_role()
        print(user_role)
        if user_role == UserRoles.Admin or user_role == UserRoles.VivaCoordinator:
            # Return all the data
            return GuideStudentMap.objects.filter(session=self.current_session)
        elif user_role == UserRoles.Tutor:
            # Return data for just the class for which the faculty is a tutor for.
            return GuideStudentMap.objects.filter(
                session=self.current_session,
                student__course_id=SessionHandler.get_user_course_id()
            )
        else:
            return []
        