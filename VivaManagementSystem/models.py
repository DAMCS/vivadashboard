"""
Contains all the Data models used throughout the system
Each class is converted to a required table
"""
from django.db import models
from PIL import Image
from util import UserRoles, ReportSubmissionStatus, SemChoices, CourseName, CourseShortName
import datetime

class VMS_Session(models.Model):
	"""
	Model to represent the various Sessions present in the system.
	A Session denotes a Year and Semester to which all the current data belongs to.
	Eg: Session of the year 2016 and Semester odd (10th Semester for the 2012 Batch).
	Lot of things have to "belong" to a particular Session.
	"""
	SEM_CHOICES = (
		('odd'	,SemChoices.odd),
		('even'	,SemChoices.even)
	)
	session_id = models.AutoField(
		primary_key=True,
		help_text='Session ID'
	)
	session_year = models.IntegerField(
		default=0,
		help_text='Session Year'
	)
	session_sem = models.CharField(
		default=SEM_CHOICES[0],
		max_length=5,
		choices=SEM_CHOICES,
		help_text='Semester Choices'
	)
	is_current = models.BooleanField(
		default=False
	)
	class Meta:
		"""
		Contains meta data for the table.
		"""
		db_table = 'VMS_Session'

class Faculty(models.Model):
	"""
	Model to represent all the different faculty in the System.
	Faculty can represent on of the following,
	1. Tutor
	2. Course Co ordinator
	3. Viva Co ordinator
	4. Guide
	#
	The Admin is not considered a Faculty
	* Admin merely manages the system.
	"""
	# The faculty ID which corelates the faculties actual
	employee_id = models.CharField(
		max_length=10,
		primary_key=True,
		help_text="Employee ID"
	)
	# Profession titles/honorifics such as Mr., Ms., Dr. and so on.
	title = models.CharField(
		max_length=4,
		help_text="Title"
	)
	# Faculty's name
	name = models.CharField(
		max_length=100,
		help_text="Faculty name"
	)
	# Faculty's Designation inside the department.
	designation = models.CharField(
		max_length=50,
		help_text="Faculty designation"
	)
	# Faculty's internal short name.
	short_name = models.CharField(
		max_length=10,
		help_text="Short name"
	)
	# Faculty's area of primary study/competency.
	core_competency = models.CharField(
		max_length=30,
		help_text="Core Competency"
	)
	# Email ID
	email_id = models.EmailField(
		default="Invalid",
		help_text="Email ID"
	)
	# Faculty's area of interest
	areas_of_interest = models.TextField(
		help_text="Areas of Interest"
	)
	# Phone number
	phone_number = models.CharField(
		max_length=13,
		help_text="Contact"
	)
	# Boolean value holds true if faculty is designated as a guide.
	is_guide = models.BooleanField(
		default=False,
		help_text="Guide?"
	)
	# Number of llocated students across all sessions.////NEED TO CHECK////
	allocated_count = models.IntegerField(
		default=0,
		help_text="Students Allocated"
	)

	def __str__(self):
		return self.employee_id + ' - ' + self.name

	class Meta:
		"""
		Meta data about the Faculty Table.
		"""
		db_table = 'Faculty'
		ordering = ['employee_id']



class User(models.Model):
	"""
	Model to hold the information of the users eligble to log into the system.
	Users in the system are given a password to log into the system.
	"""
	USER_ROLES = (
		('Administrator'	, UserRoles.Admin),
		('Viva Coordinator'	, UserRoles.VivaCoordinator),
		('Tutor'			, UserRoles.Tutor),
		('Guide'			, UserRoles.Guide),
		('Guest'			, UserRoles.Guest)
	)

	#Foreign Keys
	user = models.ForeignKey(
		Faculty,
		on_delete=models.CASCADE
	)
	session = models.ForeignKey(
		VMS_Session,
		on_delete=models.CASCADE,
		default=1
	)

	user_pass = models.CharField(
		max_length=150,
		help_text="Passcode"
	)
	user_role = models.CharField(
		max_length=50,
		choices=USER_ROLES,
		help_text="User role"
	)
	logged_in_time = models.DateTimeField(
		null=True
	)
	# As seperate schema for tutor has been removed User will carry these fields for now
	isIDFSent = models.IntegerField(
		null=True,
		default=0
	)
	isRSDFSent = models.IntegerField(
		null=True,
		default=0
	)

	#def __str__(self):
	#	return self.user_role + ' - ' + self.user_id


	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'User'
#		unique_together = ('user', 'user_role')

class Course(models.Model):
	"""
	Model that contains details about the Course provided by the System.
	They help to serve the following mappings.
	1. Each student is registered under a particular course.
	2. Each course co-ordinator is associated with a particular course.
	3. Each tutor is associated with a particular course.
	"""
	COURSE_NAME = (
		('Applied Mathematics'			,CourseName.AM),
		('Software Systems'				,CourseName.SWS),
		('Theoretical Computer Science'	,CourseName.TCS),
		('Data Science'					,CourseName.DS)
	)
	SHORT_NAME = (
		('AM'	,CourseShortName.AM),
		('SWS'	,CourseShortName.SWS),
		('TCS'	,CourseShortName.TCS),
		('DS'	,CourseShortName.DS)
	)
	course_id = models.AutoField(
		primary_key=True,
		help_text="Course ID"
	)
	degree_name = models.CharField(
		max_length=10,
		default='MSc',
		help_text="Degree"
	)
	course_name = models.CharField(
		max_length=50,
		choices=COURSE_NAME,
		default=COURSE_NAME[1],
		help_text="Available Courses"
	)
	short_name = models.CharField(
		max_length=5,
		choices=SHORT_NAME,
		default=SHORT_NAME[1],
		help_text="Course short name"
	)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'Course'
		ordering = ['course_id']

class Batch(models.Model):
	"""
	Model to denote the details of a particular course in a particular session.
	Details contained include Group mail, Class strength and the tutor for the course.
	This is required to allow the course to be provided / cancelled during each Session.
	"""

	# Foreign Keys
	# A batch belongs to a particular course
	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE
	)
	# A batch is related to a user who IS a tutor
	tutor = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	# Feilds
	# Year of joining of batch
	year = models.IntegerField(
		null=True
	)
	"""# The combined prefix 'year' + 'shortname' of batch
	batch_id = models.CharField(
		max_length=10,
		default="MSCSE2K12"
	)"""
	# Batch email id, usually a google groups mailing list
	email_id = models.EmailField(
		default="invalid@example.com"
	)
	# Strength of the batch
	strength = models.IntegerField(
		default=0
	)

	def __str__(self):
		return self.batch_id + ' - ' + str(self.tutor_id)

	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'Batch'
		ordering = ['year']


class Student(models.Model):
	"""
	Model that contains the information regarding the Students in the system.
	Information is extracted from the following Google Docs Form.
	<LINK_HERE>
	Primary key for the Students table is going to be roll_no
	"""
	SEMESTER_CHOICES = (
		(7, SemChoices.seven),
		(9, SemChoices.nine),
		(4, SemChoices.four)
	)
	PROJECT_CATEGORY_CHOICES = (
		('Industry', 'Industry Project'),
		('Research', 'Institution/Research Project')
	)
	REPORT_SUBMISSION_STATUS_CHOICES = (
		('Pending'	, ReportSubmissionStatus.Pending),
		('Submitted', ReportSubmissionStatus.Submitted)
	)
	# Primary Key
	roll_no = models.CharField(
		max_length=8,
		primary_key=True,
		help_text="Student Roll No."
	)
	# Foreign Key
	batch = models.ForeignKey(
		Batch,
		on_delete = models.CASCADE,
		default=21
	)
	# Feilds
	semester = models.IntegerField(
		choices=SEMESTER_CHOICES,
		help_text="Semester"
	)
	name = models.CharField(
		max_length=100,
		help_text="Student Name"
	)
	email_id = models.EmailField(
		default="invalid@example.com",
		help_text="Student Email ID"
	)
	photo = models.ImageField(
		blank=True,
		help_text="Student Photo"
	)
	phone_number = models.CharField(
		max_length=13,
		help_text="Student Phone Number"
	)
	project_category = models.CharField(
		max_length=20,
		choices=PROJECT_CATEGORY_CHOICES,
		blank=True,
		help_text="Project Category"
	)
	organization_name = models.CharField(
		max_length=200,
		blank=True,
		help_text="Organization"
	)
	"""
	Change to multiline
	"""
	postal_address = models.CharField(
		max_length=500,
		blank=True,
		help_text="Address"
	)
	address_short_url = models.URLField(
		blank=True,
		help_text="Organization Location URL"
	)
	address_city = models.CharField(
		max_length=300,
		blank=True,
		help_text="City"
	)
	mentor_name = models.CharField(
		max_length=100,
		blank=True,
		help_text="Mentor"
	)
	mentor_designation = models.CharField(
		max_length=100,
		blank=True,
		default="Mentor",
		help_text="Mentor's Designation"
	)
	mentor_email_id = models.EmailField(
		blank=True,
		default="invalid@example.com",
		help_text="Mentor's email ID"

	)
	domain_key_word = models.CharField(
		max_length=300,
		blank=True,
		help_text="Student's Domain"

	)
	project_title = models.CharField(
		max_length=250,
		help_text="Project Title"
	)
	join_date = models.DateField(
		help_text="Join Date"
	)
	report_submission_status = models.CharField(
		max_length=20,
		choices=REPORT_SUBMISSION_STATUS_CHOICES,
		default=REPORT_SUBMISSION_STATUS_CHOICES[0],
		help_text="Report Submission status"
	)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'Student'
		ordering = ['roll_no']



class GuideStudentMap(models.Model):
	"""
	Model to hold the mapping information between a Student and a Guide.
	A Guide is a Faculty who has a "Guide" role assigned for the current Session.
	"""

	#Foreign Keys
	session = models.ForeignKey(
		VMS_Session,
		on_delete=models.CASCADE
	)
	guide = models.ForeignKey(
		Faculty,
		on_delete=models.CASCADE
	)
	student = models.ForeignKey(
		Student,
		on_delete=models.CASCADE
	)
	# Should only default to null.
	# Why should this be -1. Defies the concept of ForeignKey.
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default="-1"
		)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'GuideStudentMap'
		unique_together = ('session', 'guide', 'student')

 