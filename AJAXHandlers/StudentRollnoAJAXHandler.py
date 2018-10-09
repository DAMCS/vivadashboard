import json
from django.http import JsonResponse
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Student, User
from util import SessionHandler


class StudentRollnoAJAXHandler(IAJAXHandler):
	'''
	AJAX Handler for getting the Student List from the Server
	'''

	def handle_request(self, http_request):
		# Check the details based on the User Session
		# Check the details based on the User Session
		roll_no = http_request.GET.get("roll_no")
		student_list = Student.objects.filter(roll_no=roll_no).values('roll_no', 'semester', 'name', 'photo', 'course_id',
																	  'email_id', 'project_category', 'postal_address',
																	  'organization_name', 'domain_key_word',
																	  'address_short_url',
																	  'phone_number', 'mentor_name',
																	  'mentor_designation', 'mentor_email_id',
																							'project_title',
																	  'domain_key_word', 'join_date', 'address_city',
																	  'report_submission_status'
																	  )
		return JsonResponse({'result': list(student_list)})
