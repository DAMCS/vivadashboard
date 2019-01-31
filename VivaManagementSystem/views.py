"""
File that is used to process all the view request
"""
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from VivaManagementSystem.models import User
from VivaManagementSystem.models import Faculty, Batch
from AJAXHandlers import AJAXHandlerFactory
from util import GenericUtil
from util import SessionHandler
from util import spreadsheet_module
from util.types import UserRoles
import json

def login(request):
	"""
	Page for logging into the system. Contains a screen to enter username and password.
	"""
	SessionHandler.set_session_obj(request.session)
	if SessionHandler.is_user_logged_in():
		return redirect("/index/")
	template = loader.get_template('newVMS/page_login.html')
	context = {}
	return HttpResponse(template.render(context, request))

def logout(request):
	"""
	Page for logging out and destroying the current session.
	"""
	SessionHandler.set_session_obj(request.session)
	SessionHandler.logout_user()
	return redirect("/login/")

def index(request):
	"""
	Index page that displays a dashboard containing all the meta information about the students.
	Page various according to the type of the user logged into the system.
	Loads different pages for different people.
	1. Dashboard for Guide -> Only shows alloted students details.
	2. Dashboard for Admin / Viva Coord / Tutor -> Shows graphs and tables.
		i. Tutor -> Only gets the details of the class for which the faculty is a tutor for.
	TODO Method is too big. Splitup everything.
	"""
	SessionHandler.set_session_obj(request.session)
	if not SessionHandler.is_user_logged_in(): # Check login status
		return redirect('/login/')
	user_id = SessionHandler.get_user_id()
	user_name = SessionHandler.get_user_name()
	isIDFSent = 0
	isRSDFSent = 0
	faculty_object = Faculty.objects.get(employee_id=user_id)
	user_object = User.objects.get(user_id=user_id) # For user_role.
	last_logged_in = user_object.logged_in_time
	print(user_object.user_id)
	user_name = faculty_object.name # For the name

	if GenericUtil.is_connected(): # TODO FIXME Move this to a AJAX Request. This severly hogs up data.
		spreadsheet_module.update_database(last_logged_in)
		user_object.logged_in_time = datetime.now()
		user_object.save()
	
	if user_object.user_role == UserRoles.Tutor.value:
		course_object = Batch.object.select_related('course').get(user_id=user_id)
		course_name = course_object.course_name
		isIDFSent = user_object.isIDFSent
		isRSDFSent = user_object.isRSDFSent
	else: # Could be an admin or just a Guide
		if user_object.user_role == UserRoles.Admin.value:
			course_name = 'Admin View'
		elif user_object.user_role == UserRoles.Guide.value:
			course_name = 'Guide View'
		else:
			course_name = 'Guest View'
	# Change the view according to the logged in user type
	context = {
		'username': user_name,
		'userrole' : str(user_object.user_role),
		'pagename': 'VMS-Index',
		'course_name': course_name,
		'is_idf_sent':isIDFSent,
		'is_rsdf_sent':isRSDFSent
	}
	if user_object.user_role != UserRoles.Guide.value:
		template = loader.get_template('newVMS/page_index.html')
		context['js_files'] = [
			'/static/newVMS/js/third-party/charts/raphaeljs.min.js',
			'/static/newVMS/js/third-party/charts/morris.min.js',
			'/static/newVMS/js/third-party/charts/chartjs.min.js',
			'/static/newVMS/js/third-party/materialize.min.js',
			'/static/newVMS/js/index/chartDrawing.js',
			"/static/newVMS/js/navbar.js"
		]
		context['css_files'] = [
			'/static/newVMS/styles/third-party/morris.css',
			'/static/newVMS/styles/third-party/materialize.min.css',
			'/static/newVMS/styles/index/custom.css'
		]
	else: # This is for guide. Show alloted students details.
		template = loader.get_template('newVMS/page_index_guide.html')
		context['js_files'] = [
			'/static/newVMS/js/third-party/materialize.min.js',
			'/static/newVMS/js/index/index-for-guide.js'
		]
		context['css_files'] = [
			'/static/newVMS/styles/third-party/materialize.min.css',
			'/static/newVMS/styles/index/custom.css'
		]
	return HttpResponse(template.render(context, request))

def config(request):
	"""
	Configuration page that is used to set critical settings for the System.
	Only certain Roles are allowed to acccess this page. They are,
	1. Administrator
	2. Viva Coordinator
	"""
	SessionHandler.set_session_obj(request.session)
	if not SessionHandler.is_user_logged_in():
		return redirect('/login/')
	template = loader.get_template('newVMS/page_config.html')

	user_id = SessionHandler.get_user_id()
	user_role = SessionHandler.get_user_role()

	faculty_object = Faculty.objects.get(employee_id=user_id)
	user_object = User.objects.select_related('user').get(user_id=user_id)
	course_object = Batch.object.select_related('course').get(user_id=user_id)
	user_name = faculty_object.name
	isIDFSent=0
	isRSDFSent=0

	if user_role == UserRoles.Admin.value:
		course_name = "Admin View"
	elif user_role == UserRoles.Guest.value:
		course_name = "Guest View"
	else:
		course_name = course_object.course_name
		isIDFSent = user_object.isIDFSent
		isRSDFSent = user_object.isRSDFSent
	# Set the email to use when setting a new Form Response Sheet
	SECRETS_FILE = 'data/VMSServiceAccountCredentials.json'
	file_data = json.load(open(SECRETS_FILE))
	context = {
		'username': user_name,
		'userrole' : str(user_role),
		'pagename': 'VMS-Config',
		'course_name': course_name,
		'google_sheets_perm_user_email': file_data['client_email'],
		'is_idf_sent': isIDFSent,
		'is_rsdf_sent': isRSDFSent,
		'js_files': [
			'/static/newVMS/js/third-party/materialize.min.js',
			'/static/newVMS/js/config/main.js',
			"/static/newVMS/js/navbar.js"
		],
		'css_files': [
			'/static/newVMS/styles/third-party/materialize.min.css',
			'/static/newVMS/styles/config/main.css'
		]
	}
	return HttpResponse(template.render(context, request))

def guide_allot(request):
	"""
	Page for handling all Guide Allotments to the various Students of the system.
	"""
	SessionHandler.set_session_obj(request.session)
	if not SessionHandler.is_user_logged_in():
		return redirect('/login/')
	template = loader.get_template('newVMS/page_guide_allot.html')
	user_id = SessionHandler.get_user_id()
	user_role = SessionHandler.get_user_role()
	
	faculty_object = Faculty.objects.get(employee_id=user_id)
	user_object = User.objects.select_related('user').get(user_id=user_id)
	course_object = Batch.object.select_related('course').get(user_id=user_id)
	user_name = faculty_object.name
	
	isIDFSent = 0
	isRSDFSent = 0

	if user_role == UserRoles.Admin.value:
		course_name = "Admin View"
		course_id = "-1"
	elif user_role == UserRoles.Guest.value:
		course_name = "Guest View"
		course_id = "-1"
	else:
		course_name = course_object.course_name
		isIDFSent = user_object.isIDFSent
		isRSDFSent = user_object.isRSDFSent
		course_id = course_object.course_id
	context = {
		'userid'  :user_id,
		'username': user_name,
		'userrole': str(user_role),
		'pagename': 'VMS-GuideAllot',
		'course_name':course_name,
		'course_id':course_id,
		'is_idf_sent': isIDFSent,
		'is_rsdf_sent': isRSDFSent,
		'css_files': [
			"/static/newVMS/styles/guide-allot.css"
		],
		'js_files': [
			'/static/newVMS/js/guide_allot.js',
			"/static/newVMS/js/navbar.js"
		]
	}
	return HttpResponse(template.render(context, request))

def guide_select(request):
	"""
	Page for selecting the various faculty to be Guides during the current session.
	"""
	SessionHandler.set_session_obj(request.session)
	if not SessionHandler.is_user_logged_in():
		return redirect('/login/')
	query_results = Faculty.objects.all()
	faculty_object = query_results.get(employee_id=user_id)
	user_object = User.objects.select_related('user').get(user_id=user_id)

	user_name = faculty_object.name
	user_role = SessionHandler.get_user_role()
	user_id = SessionHandler.get_user_id()

	isIDFSent = 0
	isRSDFSent = 0

	if user_role == UserRoles.Admin.value:
		course_name = "Admin View"
	elif user_role == UserRoles.Guest.value:
		course_name = "Guest View"
	else:
		course_name = tutors[0].course.course_name
		isIDFSent = user_object.isIDFSent
		isRSDFSent = user_object.isRSDFSent

	template = loader.get_template('newVMS/page_guide_select.html')
	context = {
		'query_results': query_results,
		'username': user_name,
		'userrole': str(user_role),
		'pagename': 'VMS-Config',
		'course_name': course_name,
		'is_idf_sent': isIDFSent,
		'is_rsdf_sent': isRSDFSent,
		'css_files':[
			"/static/newVMS/styles/guide-select/guide-select.css"
		],
		'js_files':[
			"/static/newVMS/js/guide-select/guide-select-vue.js",
			"/static/newVMS/js/navbar.js"
		]
	}
	return HttpResponse(template.render(context, request))

def ajax(request, ajax_call):
	"""
	Page to handle all AJAX calls throughout the system.
	:param request:
	:param ajax_call: Used for routing the AJAX calls.
	:return: HTTPResponse containing the result
	"""
	SessionHandler.set_session_obj(request.session)
	handler = AJAXHandlerFactory.create_instance(ajax_call)
	processed_data = handler.handle_request(request)
	return HttpResponse(processed_data)

def student_list(request):
	SessionHandler.set_session_obj(request.session)
	if not SessionHandler.is_user_logged_in():
		return redirect('/login/')
	template = loader.get_template('newVMS/page_student_list.html')
	user_id = SessionHandler.get_user_id()
	user_role = SessionHandler.get_user_role()

	user_object = User.objects.select_related('faculty').get(user_id=user_id)
	faculty_object = Faculty.objects.get(employee_id=user_id)
	course_object = Batch.object.select_related('course').get(user_id=user_id)
	user_name = faculty_object.name

	isIDFSent = 0
	isRSDFSent = 0

	if user_role == UserRoles.Admin.value:
		course_name = "Admin View"
	elif user_role == UserRoles.Guest.value:
		course_name = "Guest View"
	else:
		course_id = course_object.course_id
		isIDFSent = user_object.isIDFSent
		isRSDFSent = user_object.isRSDFSent
	context = {
		'username': user_name,
		'userrole': str(user_role),
		'pagename': 'VMS-Config',
		'course_name': course_name,
		'course_id': course_id,
		'is_idf_sent': isIDFSent,
		'is_rsdf_sent': isRSDFSent,
		'css_files': [
			"/static/newVMS/styles/student-list/student-list.css"
		],
		'js_files': [
			"/static/newVMS/js/student-list/student-list.js",
			"/static/newVMS/js/navbar.js"
		]
	}
	return HttpResponse(template.render(context, request))

def about(request):
	"""
	About page that displays the credits for the application.
	"""
	SessionHandler.set_session_obj(request.session)
	if not SessionHandler.is_user_logged_in():
		return redirect('/login/')
	template = loader.get_template('newVMS/page_about.html')
	user_id = SessionHandler.get_user_id()
	user_role = SessionHandler.get_user_role()

	user_object = User.objects.select_related('faculty').get(user_id=user_id)
	faculty_object = Faculty.objects.get(employee_id=user_id)
	user_name = faculty_object.name
	
	isIDFSent = 0
	isRSDFSent = 0

	if user_role == UserRoles.Admin.value:
		course_name = "Admin View"
	elif user_role == UserRoles.Guest.value:
		course_name = "Guest View"
	else:
		isIDFSent = user_object.isIDFSent
		isRSDFSent = user_object.isRSDFSent
	context = {
		'username': user_name,
		'userrole': str(user_role),
		'pagename': 'VMS-Config',
		'course_name': course_name,
		'is_idf_sent': isIDFSent,
		'is_rsdf_sent': isRSDFSent,
		'css_files': [
		],
		'js_files': [
			"/static/newVMS/js/navbar.js"
		]
	}
	return HttpResponse(template.render(context, request))
