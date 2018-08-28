"""
Method for handling the AJAX Login requests
"""
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import VMS_Session, Tutor, Batch

class TutorDetailsAJAXHandler(IAJAXHandler):
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
        course_data = self.get_course_tutors(active_session)

        return JsonResponse({'status': True, 'data': course_data})

    def get_course_tutors(self, active_session):
        """
        Method to retrieve the course and tutors given the active_session
        """
        course_tutor_data = []
        tutors = Tutor.objects.filter(session_id=active_session.pk)
        for tutor in tutors:
            course_strength = self.get_course_strength(tutor.course, active_session)
            course_tutor_data.append(
                {
                    'course_name' : tutor.course.course_name,
                    'tutor_name': tutor.faculty.name,
                    'strength': course_strength
                }
            )
        return course_tutor_data

    def get_course_strength(self, course, active_session):
        """
        Method to retrieve the strength of the course during a particular session
        """
        # Get the Batch using the Course and VMS Session
        batch = Batch.objects.get(course=course, session=active_session)
        if batch is None:
            return -1
        else:
            return batch.strength
