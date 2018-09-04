"""
Contains all the Data models used throughout the system
Each class is converted to a required table
"""
from django.db import models
from util import UserRoles, ReportSubmissionStatus

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
    session_id = models.IntegerField(primary_key=True,help_text='Session ID')
    session_year = models.IntegerField(default=0,help_text='Session Year')
    session_sem = models.CharField(default=SEM_CHOICES[0],max_length=5, choices=SEM_CHOICES,help_text='Semester Choices')
    is_current = models.BooleanField(default=False)
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
    employee_id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)
    core_competency = models.CharField(max_length=30)
    email_id = models.EmailField(default="Invalid")
    areas_of_interest = models.TextField()
    phone_number = models.CharField(max_length=13)
    is_guide = models.BooleanField(default=False)
    allocated_count = models.IntegerField(default=0)
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
    course_id = models.AutoField(primary_key=True)
    degree_name = models.CharField(max_length=10, default='MSc')
    course_name = models.CharField(max_length=50, choices=COURSE_NAME, default=COURSE_NAME[1])
    short_name = models.CharField(max_length=5, choices=SHORT_NAME, default=SHORT_NAME[1])
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
    roll_no = models.CharField(max_length=8, primary_key=True)
    # Foreign Key
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    session = models.ForeignKey(VMS_Session, on_delete=models.CASCADE, default=None, null=True)
    # Others
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    name = models.CharField(max_length=100)
    email_id = models.EmailField(default="Invalid")
    phone_number = models.CharField(max_length=13)
    project_category = models.CharField(max_length=20, choices=PROJECT_CATEGORY_CHOICES, blank=True)
    organization_name = models.CharField(max_length=200, blank=True)
    postal_address = models.CharField(max_length=500, blank=True)
    address_short_url = models.CharField(max_length=200, blank=True)
    address_city = models.CharField(max_length=300, blank=True)
    mentor_name = models.CharField(max_length=100, blank=True)
    mentor_designation = models.CharField(max_length=100, blank=True)
    mentor_email_id = models.EmailField(blank=True)
    domain_key_word = models.CharField(max_length=300, blank=True)
    project_title = models.CharField(max_length=500, blank=True)
    join_date = models.CharField(max_length=10, blank=True)
    report_submission_status = models.CharField(max_length=20, default='Pending', blank=False)
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
    session = models.ForeignKey(VMS_Session, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    year = models.IntegerField(null=True)
    email_id = models.EmailField(default="Invalid")
    strength = models.IntegerField(default=0)
    tutor = models.ForeignKey(Faculty, on_delete=models.CASCADE)
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
    session = models.ForeignKey(VMS_Session, on_delete=models.CASCADE, default=None)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #MADE CHANGES DURING MIGRATION
    isIDFSent = models.IntegerField(null=True)
    isRSDFSent = models.IntegerField(null=True)
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
    user = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    user_pass = models.CharField(max_length=150)
    user_role = models.CharField(max_length=50, choices=ALLOWED_USER_ROLES)
    logged_in_time = models.DateTimeField(null=True, blank=True, default=None)
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
    session = models.ForeignKey(VMS_Session, on_delete=models.CASCADE, default=None)
    guide = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # Should only default to null.
    # Why should this be -1. Defies the concept of ForiengKey.
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, default="-1")
    class Meta:
        """
        Class that contains the information about the Table.
        """
        db_table = 'GuideStudentMap'
        unique_together = ('session', 'guide', 'student')
