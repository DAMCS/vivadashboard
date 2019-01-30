"""
Module that contains the grouping of various configuration keys used to store important information
"""
from enum import Enum

class GoogleSheetConfigKeys(Enum):
	'''
	Contains the Keys used with reference at the Google Sheet details
	'''
	# This is for Students Form
	StudentsFormName = 'StudentInternshipDetails'
	StudentsFormURL = 'StudentsFormURL'
	# This is for Faculty Form
	FacultyFormName = 'FacultyInformation'
	FacultyFormURL = 'FacultyFormURL'
	# This is for Report Submission Status
	ReportSubmissionFormName = 'ProjectReportDetails'
	ReportSubmissionFormURL = 'ReportSubmissionFormURL'
