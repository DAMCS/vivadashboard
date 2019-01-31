"""
Method for handling the AJAX Login requests
"""
import json
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import User, Batch
from util.SessionHandler import SessionHandler
from util.types import UserRoles

class LoginAJAXHandler(IAJAXHandler):
	'''
	AJAXHandler for dealing with the login process.
	'''

	def handle_request(self, http_request):
		"""Recieves Login Request

		:param http_request:
		:return json_dump:
		"""
		userid = http_request.POST['userid']
		password = http_request.POST['password']
		try:
			result = dict()
			result['status'] = 'fail'
			if SessionHandler.is_user_logged_in():
				result['msg'] = 'User already logged in. Logout and try again.'
			try:
				user_object = User.objects.get(user_id = userid, user_pass = password)
				SessionHandler.login_user(user_object)
				result['status'] = 'success'
			except User.DoesNotExist:
				print(Exception)
				result['msg'] = '!! Invalid Credentials!'
		except Exception:
			print(Exception)
			result['msg'] = '!! Unhandled Exception! Contact System Administrators'
		return json.dumps(result)
'''
	def handle_request(self, http_request):
		"""
		Gets the username and password from the Request and then validates them from the DB
		:param http_request:
		:return: JSON response with the valid flag
		"""
		# Make the userid case insensitive
		userid = http_request.POST['userid']
		password = http_request.POST['password']
		result = dict()
		result['status'] = 'fail'
		if SessionHandler.is_user_logged_in():
			result['msg'] = 'User already logged in. Logout and try again.'
			return json.dumps(result)
		try:
			# TODO Changing this to case insensitive is causing issues everywhere else. Enforce all caps user names
			user_obj = User.objects.get(user_id=userid, user_pass=password)
			tutor_obj = Batch.objects.select_related('tutor').filter(tutor=user_obj.user_id)
			# This is causing a error since the logged in faculty could also be an
			# Admin who is not a tutor for any course
			course_id = None
			if len(tutor_obj) > 0:
				course_id = tutor_obj[0].course.course_id
			user_obj.course_id = course_id # Used for creating the session.
			SessionHandler.login_user(user_obj)
			result['course_id'] = course_id
			result['status'] = 'success'
			result['role'] = user_obj.user_role
		except User.DoesNotExist:
			# Invalid user. Return error message
			result['msg'] = 'Invalid credentials.'
		# JSON Encode the results and send it back
		return json.dumps(result)
'''