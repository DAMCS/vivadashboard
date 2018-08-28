import json
import smtplib
from AJAXHandlers.IAJAXHandler import IAJAXHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from VivaManagementSystem.models import Tutor, Faculty
from util import SessionHandler

MAIL_CONTENT_FILE_PATH = 'data/mailContent.json'
def sendEmail(mail_id, text,subject):
    print(mail_id)
    fromaddr = 'gowri.jshankar@gmail.com'
    toaddrs = 's.prakash10010@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg.attach(MIMEText(text, 'plain'))
    username = 'gowri.jshankar'
    password = 'leelavathi'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

    return


def sendMailToGuide(mainContent,guide_mail_id, rollno, name_list, student_email_id, length):
    i = 0
   # text = "You are allocated the following students(RollNo, Name, MailId) to guide on their projects : "
    mainContent=mainContent.replace("{no}",str(length))
    text=""
    while i < length:
        text = text + "\n" + rollno[i] + "  " + name_list[i] + "   " + student_email_id[i]
        i = i + 1
    mainContent=mainContent.replace("{students}", text)
    print(mainContent)
    #sendEmail(guide_mail_id, text,"Guide Allocation Notification!!!")
    return


def sendMailToStudent(mainContent,guide_no, guide_mail_id, stud_email_temp):
    #text = title + " " + guide_name + " has been allocated as your guide. " + "Contact at " + guide_mail_id + "."
    text=mainContent.replace("{guide_no}",guide_no)
    text = text.replace("{guide_mail}", guide_mail_id)
    #print(text)
    #sendEmail(stud_email_temp, text,"Guide Allocation Notification!!!")
    return


class SendMailAJAXHandler(IAJAXHandler):
    '''
    AJAX Handler for getting the Student List from the Server
    '''

    def handle_request(self, http_request):
        # Check the details based on the User Session
        # Check the details based on the User Session
        mailContent=json.load(open(MAIL_CONTENT_FILE_PATH))
        current_user_id = SessionHandler.get_user_id()
        myTutor=Tutor.objects.get(faculty_id=current_user_id)
        course_name=myTutor.course.degree_name+" "+myTutor.course.course_name
        map_dict = http_request.POST.get("map_dict")
        data = json.loads(map_dict)
        for guide_key in data:
            guide=Faculty.objects.get(employee_id=guide_key)
            guide_designation=guide.designation
            guide_title=guide.title
            guide_no=guide.phone_number
            guide_obj = data[guide_key]
            name_list = []
            student_email_id = []
            rollno = []
            guide_mail_id = guide_obj[0]['studentObj']['guide_email_id']
            guide_name = guide_obj[0]['studentObj']['guide_name']
            title = guide_obj[0]['studentObj']['title']
            length = 0

            for stud_obj in guide_obj:
                stud_email_temp = stud_obj['studentObj']['student_email_id']
                student_email_id.append(stud_email_temp)
                name_list.append(stud_obj['studentObj']['name'])
                rollno.append(stud_obj['student'])
                length = length + 1
                sendMailToStudent(mailContent['studentMail'].replace("{guide}",guide_title+" "+guide_name+" "+guide_designation),guide_no, guide_mail_id, stud_email_temp)

            sendMailToGuide(mailContent['guideMail'].replace("{course}",course_name),guide_mail_id, rollno, name_list, student_email_id, length)

        return json.dumps(map_dict)