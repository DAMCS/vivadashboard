/**
 * Index page displayed for a Faculty who is only a Guide in the system.
 * Only displays information regarding the students allotted to the Faculty.
 */
window.indexGuideVue = new Vue({
    el: '#vue_alloted_students_list',
    data: {
        students: [],
        hasStudentList: false
    }
});
$(document).ready(function(){
    $.ajax({
        url: '/ajax/alloted_student_details',
        type: 'GET',
        success: function (data) {
            jsonData = jQuery.parseJSON(data);
            if (jsonData.status) {
                window.indexGuideVue.students = jsonData.data;
                window.indexGuideVue.hasStudentList = jsonData.data.length > 0;
            } else {
                toastr.warning(jsonData.error);
            }
        }
    });
});
