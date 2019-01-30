import pandas as pd
import json

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from VivaManagementSystem.models import Faculty, VMS_Session
from VivaManagementSystem.models import Student
from VivaManagementSystem.models import Course
from util.configuration import ConfigurationManager, GoogleSheetConfigKeys
from util import ReportSubmissionStatus
#-------------------Donot change the code above this line---------------------------------

def update_faculty_records(last_logged_time):
	'''
	Updates the Faculty records from the Sheet
	'''
	# faculty_records_file = 'https://docs.google.com/spreadsheets/d/1FG3kkhmmZDooNyqCbNyRFHeTP0xYD1RqUssXFN_u9NU/edit#gid=1592165263'
	config_manager = ConfigurationManager.get_instance()
	faculty_records_file = config_manager.get_config('FacultyFormName')
	workbook = authorize_open_sheet(faculty_records_file)
	if workbook is None:
		print("Faculty Sheet cannot be opened. Debug further for more information.")
		print(faculty_records_file)
		return
	# Check if we need to update the sheet
	sheet = workbook.sheet1
	#if not can_update_sheet(sheet, GoogleSheetConfigKeys.FacultyFormName.value):
	#	print(GoogleSheetConfigKeys.FacultyFormName.value + ' form is up to date')
	#	return
	print("updating faculty data")
	# Extract all data into a dataframe
	faculty_data = pd.DataFrame(sheet.get_all_records())
	num_db_records = len(Faculty.objects.all())
	try:
		# Append rows to the Database
		for index, row in faculty_data.loc[num_db_records:].iterrows():
			model = Faculty()
			model.title = row['Title']
			model.name = row['Full Name'].upper()
			model.designation = row['Designation']
			model.short_name = row['Short Name used in Department'].upper()
			model.employee_id = row['Employee ID'].upper()
			model.core_competency = row['Core Competency']
			model.is_guide = 0
			model.students_allocated = 0
			model.email_id = row['E-mail ID']
			model.areas_of_interest = row['Area of Interest for project guidance']
			model.phone_number = row['Phone number']
			model.save()
	except:
		pass
	# Update the last checked time
	update_last_check_time(GoogleSheetConfigKeys.FacultyFormName.value)


def update_student_records(last_logged_time):
	'''
	Updates the students data from sheet
	'''
	#students_file_url = 'https://docs.google.com/spreadsheets/d/1iRx9uwfa6CYjVEtOcta4s-4qM8cDwDo8Vre6bQyTwzw/edit#gid=1893222149'
	config_manager = ConfigurationManager.get_instance()
	students_file_name = config_manager.get_config('StudentFormName')
	workbook = authorize_open_sheet(students_file_name)
	if workbook is None:
		print("Student Sheet cannot be opened. Debug further for more information.")
		print(students_file_name)
		return
	# Get the first sheet
	sheet = workbook.sheet1
	#if not can_update_sheet(sheet, GoogleSheetConfigKeys.StudentsFormName.value):
	#	print(GoogleSheetConfigKeys.StudentsFormName.value + ' form is up to date')
	#	return

	print("updating student data")
	# Extract all data into a dataframe
	student_data = pd.DataFrame(sheet.get_all_records())
	num_db_records = Student.objects.all().count()
	course_details = list(Course.objects.all().values('course_id', 'course_name'))
	course_dict = dict(zip([str(x['course_name']) for x in course_details], [int(x['course_id']) for x in course_details]))
	semester = {'VII' : 7, 'IV' : 4, 'X' : 10}
	print(student_data)
	try:
		# Append rows to the Database
		for index, row in student_data.loc[num_db_records:].iterrows():
			model = Student()
			model.roll_no = row['Roll Number'].upper()
			model.course_id = course_dict[row['MSc Programme']]
			model.semester = semester[row['Semester']]
			model.name = row['Name (as per college record)'].upper()
			model.email_id = row['Your E-Mail ID']
			model.phone_number = row['Mobile Number']
			model.photo = row['Photo']
			model.project_category = row['Project Category']
			model.organization_name = row['Name of the Organization']
			model.address_short_url = row['Short URL for Google Map / Location of the Organization']
			model.postal_address = row['Full Postal Address of the Organization']
			model.mentor_name = row['Name of the Mentor']
			model.mentor_designation = row["Mentor's Designation / Team / BU name"]
			model.mentor_email_id = row['Email of the Mentor']
			model.domain_key_word = row["Project's Domain Key words"]
			model.project_title = row['Tentative Project Title']
			model.join_date = row['Joined Date']
			model.session = VMS_Session.objects.get(is_current=1)
			model.save()
	except IndexError:
		pass
	# Update the
	update_last_check_time(GoogleSheetConfigKeys.StudentsFormName.value)


def update_report_submission_status(last_logged_time):
	'''Updates the "report_submission_status" field in the Students Table

	:param last_logged_time: ?

	:return: None
	'''
	# report_submission_sheet = 'https://docs.google.com/spreadsheets/d/1sZGYNcdb0SFAI3LY1hBlnC9YjUNytcmh-ng_pO_-jwA/edit#gid=459423118'
	config_manager = ConfigurationManager.get_instance()
	report_submission_sheet = config_manager.get_config('ReportFormName')
	workbook = authorize_open_sheet(report_submission_sheet)
	if workbook is None:
		print("Report Submission Sheet cannot be opened. Debug further for more information.")
		return
	submission_sheet = workbook.sheet1
	#if not can_update_sheet(submission_sheet, GoogleSheetConfigKeys.ReportSubmissionFormName.value):
	#	print(GoogleSheetConfigKeys.ReportSubmissionFormName.value + ' form is up to date')
	#	return
	# Proceed with updation.
	report_data = pd.DataFrame(submission_sheet.get_all_records())
	try:
		for index, row in report_data.loc[0:].iterrows():
			# Update the data here.
			student_roll = row['Roll Number'].upper()
			try:
				req_student_data = Student.objects.get(roll_no=student_roll)
			except ObjectDoesNotExist:
				continue
			# Update the data
			req_student_data.report_submission_status = ReportSubmissionStatus.Submitted.value
			req_student_data.save()
	except IndexError:
		print("Index error in forum")
	# Update the
	update_last_check_time(GoogleSheetConfigKeys.ReportSubmissionFormName.value)

def update_last_check_time(workbook_name):
	'''
	Sets the last check time in the Configuration to the current time for the given workbook_name

	:param workbook_name: Local name of the workbook to update.

	:return: None
	'''
	config_name = workbook_name + '_last_update'
	config_manager = ConfigurationManager.get_instance()
	config_manager.set_config(config_name, datetime.now().__str__())

def can_update_sheet(sheet, sheet_name):
	'''
	Checks if the report submission data can be updated in the table.
	Checks the last update time of the sheet and the config data.

	:param sheet: Sheet from gspread module's Workbook

	:param sheet_name: Local name used to refer to the sheet

	:return: :True: if last_update_time is more recent than the stored config data.
			 :False: otherwise.
	'''
	config_name = sheet_name + '_last_update'
	config_manager = ConfigurationManager.get_instance()
	last_check_value = config_manager.get_config(config_name)
	if last_check_value is None:
		# First time with the current DB
		return True
	# Check the datetime
	last_check_time = datetime.strptime(last_check_value, '%Y-%m-%d %H:%M:%S.%f')
	sheet_last_update_time = datetime.strptime(sheet.updated[:-1], '%Y-%m-%dT%H:%M:%S.%f')
	if sheet_last_update_time > last_check_time:
		return True
	print(sheet_name)
	print(last_check_value)
	print(sheet.updated[:-1])
	return False


def authorize_open_sheet(sheet_name):
	"""Authorizes the user and returns an instance of the worksheet specified by the sheet_url.

	:param sheet_url: URL pointing to the sheet in drive.

	:return: Result of open_by_url, None if the spread sheet does not exist.
	"""
	SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
	credentials = ServiceAccountCredentials.from_json_keyfile_name('data/VMSServiceAccountCredentials.json', SCOPE)
	gc = gspread.authorize(credentials)
	workbook = gc.open(sheet_name)
	return workbook

def update_database(last_logged_time):
	"""
	Updates the database with the records from all the various spreadsheets.
	"""
	update_faculty_records(last_logged_time)
	update_student_records(last_logged_time)
	update_report_submission_status(last_logged_time)
