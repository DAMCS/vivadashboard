"""
Module that contains the grouping of various configuration keys used to store important information
"""
from enum import Enum

class GoogleSheetConfigKeys(Enum):
	'''
	Contains the Keys used with reference at the Google Sheet details
	'''
	# This is for Students Form
	StudentSheetName = 'StudentSheetName'
	StudentSheetURL = 'StudentSheetURL'
	# This is for Faculty Form
	FacultySheetName = 'FacultySheetName'
	FacultySheetURL = 'FacultySheetURL'
	# This is for Report Submission Status
	ReportSubmissionSheetName = 'ReportSubmissionSheetName'
	ReportSubmissionSheetURL = 'ReportSubmissionSheetURL'
