import json
from django.http import JsonResponse
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from AJAXHandlers.SendMailAJAXHandler import sendEmail
from VivaManagementSystem.models import Batch,User
from util import SessionHandler

__FORM_CONFIG_FILE_PATH = 'data/googleForms.json'

def getBatchMailId():
	current_user_id = SessionHandler.get_user_id()
	current_batch = Batch.objects.get(tutor_id=current_user_id)
	return current_batch.email_id

def getFormLink(form_name):
	form_config=json.load(open(__FORM_CONFIG_FILE_PATH))
	return form_config[form_name]

class GoogleFormSendingAJAXHandler(IAJAXHandler):
	def handle_request(self, http_request):
		form_name = http_request.POST.get("form_name")
		form_link = getFormLink(form_name)
		is_reminder=int(http_request.POST.get("is_reminder"))
		if(is_reminder>0):
			text = "Reminder!!! Please fill the following form if you haven't done yet!!!\n\n" + form_link + "\n"
		else:
			text = "Please fill this google form as soon as possible!!!\n\n" + form_link + "\n"
		print(text)
		current_user_id = SessionHandler.get_user_id()
		if(form_name=="internship_details_form"):
			Tutor.objects.filter(faculty_id=current_user_id).update(isIDFSent=is_reminder)
		elif(form_name=="report_submission_details_form"):
			Tutor.objects.filter(faculty_id=current_user_id).update(isRSDFSent=is_reminder)
		#sendEmail(getBatchMailId(),text)
		return JsonResponse({'result':  'success'})
