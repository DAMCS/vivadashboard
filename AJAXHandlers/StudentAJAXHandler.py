from django.http import JsonResponse
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Student, User
from util import SessionHandler

class StudentAJAXHandler(IAJAXHandler):
	'''
	AJAX Handler for getting the Student List from the Server
	'''
	def handle_request(self, http_request):
		# Check the details based on the User Session
		#session_id = http_request.GET.get("session_id")
		course_id = http_request.GET.get("course_id")
		user_role = http_request.GET.get("user_role")

		if course_id == -1 or str(user_role) == "UserRoles.Admin":
			student_list = Student.objects.all().values('roll_no', 'name', 'photo','course_id','organization_name', 'domain_key_word','address_city','phone_number','email_id').order_by('roll_no')
		else:
			student_list = Student.objects.filter(course_id=course_id).values('roll_no', 'name', 'photo', 'course_id','organization_name', 'domain_key_word','address_city','phone_number', 'email_id').order_by('roll_no')
		return JsonResponse({'result': list(student_list)})
