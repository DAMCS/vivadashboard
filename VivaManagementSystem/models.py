"""
Contains all the Data models used throughout the system
Each class is converted to a required table
"""
from django.db import models
from util import UserRoles, ReportSubmissionStatus
import datetime

class VMS_Session(models.Model):
	"""
	Model to represent the various Sessions present in the system.
	A Session denotes a Year and Semester to which all the current data belongs to.
	Eg: Session of the year 2016 and Semester odd (10th Semester for the 2012 Batch).
	Lot of things have to "belong" to a particular Session.
	"""
	SEM_CHOICES = (
		('odd' , 'odd' ),
		('even', 'even')
	)
	session_id = models.IntegerField(
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
	"""
	employee_id = models.CharField(
		max_length=10,
		primary_key=True,
		help_text="Employee ID"
	)
	title = models.CharField(
		max_length=4,
		help_text="Title"
	)
	name = models.CharField(
		max_length=100,
		help_text="Faculty name"
	)
	designation = models.CharField(
		max_length=50,
		help_text="Faculty designation"
	)
	short_name = models.CharField(
		max_length=10,
		help_text="Short name"
	)
	core_competency = models.CharField(
		max_length=30,
		help_text="Core Competency"
	)
	email_id = models.EmailField(
		default="Invalid",
		help_text="Email ID"
	)
	areas_of_interest = models.TextField(
		help_text="Areas of Interest"
	)
	phone_number = models.CharField(
		max_length=13,
		help_text="Contact"
	)
	is_guide = models.BooleanField(
		default=False,
		help_text="Guide?"
	)
	allocated_count = models.IntegerField(
		default=0,
		help_text="Students Allocated"
	)
	class Meta:
		"""
		Meta data about the Faculty Table.
		"""
		db_table = 'Faculty'
		ordering = ['employee_id']

class Course(models.Model):
	"""
	Model that contains details about the Course provided by the System.
	They help to serve the following mappings.
	1. Each student is registered under a particular course.
	2. Each course co-ordinator is associated with a particular course.
	3. Each tutor is associated with a particular course.
	"""
	COURSE_NAME = (
		('Applied Mathematics', 'Applied Mathematics'),
		('Software Systems', 'Software Systems'),
		('Theoretical Computer Science','Theoretical Computer Science'),
		('Data Science','Data Science')
	)
	SHORT_NAME = (
		('AM', 'AM'),
		('SWS', 'SWS'),
		('TCS','TCS'),
		('DS','DS')
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

class Student(models.Model):
	"""
	Model that contains the information regarding the Students in the system.
	Information is extracted from the following Google Docs Form.
	<LINK_HERE>
	Primary key for the Students table is going to be roll_no
	"""
	SEMESTER_CHOICES = (
		(7, '7'),
		(9, '9'),
		(4, '4')
	)
	PROJECT_CATEGORY_CHOICES = (
		('Industry', 'Industry Project'),
		('Research', 'Institution/Research Project'),
	)
	REPORT_SUBMISSION_STATUS_CHOICES = (
		('Pending', ReportSubmissionStatus.Pending),
		('Submitted', ReportSubmissionStatus.Submitted),
	)
	# Primary Key
	roll_no = models.CharField(
		max_length=8,
		primary_key=True,
		help_text="Student Roll No."
	)
	# Foreign Key
	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE
	)
	session = models.ForeignKey(
		VMS_Session,
		on_delete=models.CASCADE,
		default=None,
		null=True
	)
	# Others
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
		default=datetime.date.today,
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

class Batch(models.Model):
	"""
	Model to denote the details of a particular course in a particular session.
	Details contained include Group mail, Class strength and the tutor for the course.
	This is required to allow the course to be provided / cancelled during each Session.
	"""

	#Foreign Keys
	session = models.ForeignKey(
		VMS_Session,
		on_delete=models.CASCADE
	)
	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE
	)
	tutor = models.ForeignKey(
		Faculty,
		on_delete=models.CASCADE
	)
	year = models.IntegerField(
		null=True
	)
	email_id = models.EmailField(
		default="invalid@example.com"
	)
	strength = models.IntegerField(
		default=0
	)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'Batch'
		unique_together = ('session', 'course')

class Tutor(models.Model):
	"""
	Model to denote the tutor for each of the course in the given session.
	This model is not required as the same information is available in the Batch table.
	TODO Remove this Model. Remove all uses of this table.
	"""

	#Foreign Keys
	session = models.ForeignKey(
		VMS_Session,
		on_delete=models.CASCADE,
		default=None
	)
	faculty = models.ForeignKey(
		Faculty,
		on_delete=models.CASCADE
	)
	course = models.ForeignKey(
		Course,
		on_delete=models.CASCADE
	)

	#Fields
	isIDFSent = models.IntegerField(
		null=True
	)
	isRSDFSent = models.IntegerField(
		null=True
	)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'Tutor'
		unique_together = ('session', 'faculty', 'course')

class User(models.Model):
	"""
	Model to hold the information of the users eligble to log into the system.
	Users in the system are given a password to log into the system.
	"""
	ALLOWED_USER_ROLES = (
		('Administrator', UserRoles.Admin),
		('Viva Coordinator', UserRoles.VivaCoordinator),
		('Tutor', UserRoles.Tutor),
		('Guide', UserRoles.Guide),
		('Guest', UserRoles.Guest)
	)

	#Foreign Keys
	user = models.ForeignKey(
		Faculty,
		on_delete=models.CASCADE
	)

	#Fields
	user_pass = models.CharField(
		max_length=150,
		help_text="Passcode"
	)
	user_role = models.CharField(
		max_length=50,
		choices=ALLOWED_USER_ROLES,
		help_text="User role"
	)
	logged_in_time = models.DateTimeField(
		null=True,
		blank=True,
		default=None
	)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'User'
		unique_together = ('user', 'user_role')

class GuideStudentMap(models.Model):
	"""
	Model to hold the mapping information between a Student and a Guide.
	A Guide is a Faculty who has a "Guide" role assigned for the current Session.
	"""

	#Foreign Keys
	session = models.ForeignKey(
		VMS_Session,
		on_delete=models.CASCADE,
		default=None
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
	# Why should this be -1. Defies the concept of ForiengKey.
	tutor = models.ForeignKey(
		Tutor,
		on_delete=models.CASCADE,
		default="-1"
		)
	class Meta:
		"""
		Class that contains the information about the Table.
		"""
		db_table = 'GuideStudentMap'
		unique_together = ('session', 'guide', 'student')
