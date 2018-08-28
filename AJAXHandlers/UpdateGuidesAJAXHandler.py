from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Faculty, Batch, User
from util.ModelUtils import ModelUtils
from util.types import UserRoles
from django.http import JsonResponse
from django.core import serializers

class UpdateGuidesAJAXHandler(IAJAXHandler):
    '''
    Updates the status of faculty (To be guide or not)
    Creates credentials for the Faculty if not exists
    '''
    def handle_request(self, http_request):
        data = http_request.POST.getlist("input[]")
        Faculty.objects.update(is_guide=0)
        for faculty_id in data:
            guide = Faculty.objects.get(employee_id=faculty_id)
            guide.is_guide = 1
            guide.save()
            # Create a credential for the User if not exists
            self.check_user_credentials_exists(guide)
        faculty_list = list(Faculty.objects.all())
        guide_count = sum(faculty.is_guide for faculty in faculty_list)
        students_count = sum((x.strength for x in Batch.objects.all()))
        if guide_count == 0:
            guide_count = 1
        recommended_count = students_count / guide_count
        return JsonResponse({
            'result': serializers.serialize('python', faculty_list),
            'rc': int(recommended_count)
        })

    def check_user_credentials_exists(self, faculty):
        """Checks if the Faculty has a login credential.
        If not available, it creates a Login Credential with username and password as Faculty ID
        """
        if User.objects.filter(user__employee_id=faculty.employee_id).count() > 0:
            print('User already exists')
        else:
            print('No Such user exists')
            ModelUtils.create_credentials_for_faculty(faculty, UserRoles.Guide.value)
