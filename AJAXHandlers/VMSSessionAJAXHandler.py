from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import VMS_Session
from django.http import JsonResponse
from django.core import serializers

class VMSSessionAJAXHandler(IAJAXHandler):
    def handle_request(self, http_request):
        action = http_request.POST['action']
        session_year = http_request.POST['session_year']
        session_sem = http_request.POST['session_sem']
        currentSession = VMS_Session()
        if action == "add":
            sessions = VMS_Session.objects.all()
            for session in sessions:
                session.is_current=False
                session.save()
            newSession = VMS_Session(session_year=session_year,session_sem=session_sem,is_current=True)
            newSession.save()
        if action == "get":
            try:
                currentSession = VMS_Session.objects.get(is_current=True)
            except currentSession.DoesNotExist:
                currentSession = None
                return JsonResponse({'result': 'none'})
            return JsonResponse({'result':  serializers.serialize('json',[currentSession])})
        return JsonResponse({'result': 'success'})
