"""
Module that contains the grouping of various configuration keys used to store important information
"""
from enum import Enum

class GoogleSheetConfigKeys(Enum):
    '''
    Contains the Keys used with reference ot the Google Sheet details
    '''
    # This is for Students Form
    StudentsFormName = 'StudentsForm'
    StudentsFormURL = 'StudentsFormURL'
    # This is for Faculty Form
    FacultyFormName = 'FacultyForm'
    FacultyFormURL = 'FacultyFormURL'
    # This is for Report Submission Status
    ReportSubmissionFormName = 'ReportSubmissionForm'
    ReportSubmissionFormURL = 'ReportSubmissionFormURL'
