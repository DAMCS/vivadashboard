import json
from django.http import JsonResponse
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from VivaManagementSystem.models import Faculty, GuideStudentMap
from util import SessionHandler


class AllottedGuideListAJAXHandler(IAJAXHandler):


    def handle_request(self, http_request):
        user_role = SessionHandler.get_user_role()



        guides = Faculty.objects.select_related().filter(is_guide=True)

        if len(guides) == 0:
            return JsonResponse({'map_data' : 'no data'})
        map = None
        map_dict = dict()
        for iter_guide in guides:
            mapped_data = GuideStudentMap.objects.select_related('guide').filter(session__session_id=1, guide=iter_guide)
            mapped_students = []
            class student_detail(object):
                student = None
                tutor = None
                course = None


            for data in mapped_data:

                student_obj = student_detail()
                student_obj.student = data.student
                student_obj.tutor = data.tutor.faculty.employee_id
                student_obj.course = data.tutor.course.course_name
                student_obj.guide_email_id = data.guide.email_id
                student_obj.guide_name = data.guide.name
                student_obj.title = data.guide.title
                mapped_students.append(student_obj)
            mapped_students.sort(key=lambda x: x.course, reverse=False)
            map_dict[iter_guide.employee_id] = mapped_students

        return JsonResponse({'map_data': json.dumps(map_dict, default=AllottedGuideListAJAXHandler.serialize)})

    @staticmethod
    def serialize(obj):
        return {
            "student" : obj.student.roll_no,
            "studentObj": dict(name=obj.student.name,organization_name=obj.student.organization_name,
                               student_email_id=obj.student.email_id,guide_email_id=obj.guide_email_id,
                               guide_name=obj.guide_name, title=obj.title),
            "tutor": obj.tutor
            #  "course":obj.course
        }
