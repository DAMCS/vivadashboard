/**
 * Created by PRASANNA on 12/28/2016 and modified by Akhilesh R on 09/17/2018
 */

var course_id ;
var user_role;

function students_search() {
  var input, filter, table, tr, td, i;
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  student_list = document.getElementById("student-list");
  rows = student_list.getElementsByTagName("header");
  divs = $(document.getElementById("student-list")).children()
  for (i = 0; i < rows.length; i++) {
    data = rows[i].getElementsByTagName("h3")[0];
    data1=rows[i].getElementsByTagName("h5")[0];
    if (data && data1) {
      if ((data.innerHTML.toUpperCase().indexOf(filter) > -1)|| (data1.innerHTML.toUpperCase().indexOf(filter)>-1)){
        divs[i].style.display = "";
      } else {
        divs[i].style.display = "none";
      }
    }
  }
}
$(document).ready(function(){
    $("#container").mCustomScrollbar({
        theme:"3d",
        scrollbarPosition: "inside"

    });
    course_id = $("#course-id").val();
    user_role = $("#user_role").val();
});

function closeModal() {
    $('.student_popup').css("display","none");
    $('#student-list').css("filter","blur(0px)");
}


function UpdateStudentList(data){
    var student_record;
    $.each(data, function(i, item) {
        student_record = '<div class="w3-card-4 student" id="w3-card-4">'+'<div class="image"></div>'+'<header class="w3-container"><h3>'+item.name+'</h3><h5 id="roll_no">'+item.roll_no+'</h5>'+'<p class="organization-name">'+ item.organization_name+', '+item.address_city+'<br>'+ item.phone_number+ '<br>'+'</p></div>';
        $('#student-list').append(student_record);
    });
    $(".student").click(function() {
        roll_no = $(this).find('#roll_no')[0].innerText;
        $.ajax({
            type: "GET",
            url: '/ajax/get_student?roll_no='+roll_no,
            success: function(result) {
                result = JSON.parse(result);
                $.each(result["result"], function(i, item) {
                    student_record =
                        '<span class="close" onclick="closeModal()">&times;</span>' +
                        '<div class="w3-card-16 student_detail" id="w3-card-16">' +
                            '<div class="w3-container">' +
                                '<h3>'+item.name+'</h3>' +
                                '<h5>'+item.roll_no+'</h5>'+'' +
                                 '' +
                                '<table style="width:100%">' +
                                    '<tr>' +
                                        '<td>' +
                                        'Semester' +
                                        '<td>' +
                                        item.semester+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Email ID' +
                                        '<td>' +
                                        item.email_id+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Mobile' +
                                        '<td>' +
                                        item.phone_number+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Project Category' +
                                        '<td>' +
                                        item.project_category+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Organization Name' +
                                        '<td>' +
                                        item.organization_name+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Mentor Name' +
                                        '<td>' +
                                        item.mentor_name+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Mentor Designation' +
                                        '<td>' +
                                        item.mentor_designation+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Project Title' +
                                        '<td>' +
                                        item.project_title+
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td>' +
                                        'Report Submission Status' +
                                        '<td>' +
                                        item.report_submission_status+
                                        '</td>' +
                                    '</tr>' +
                                '</table>' +
                        '</div>';
                    $('.student_popup').html(student_record);
                    $('.student_popup').css("display","block");
                    $('#student-list').css("filter","blur(20px)");
                    $(".student_popup").show();

                    //$('#container').hide()
                });
            }
        });
    });
}
$(document).ready(function(){
   $.ajax({
       type: "GET",
       url: '/ajax/get_student_list?course_id='+course_id+'&'+'user_role='+user_role,
       error: function (err) {
            alert("Error in Student details retrieval " + err.responseText);
        },
        success: function(result) {
        console.log("Success");
           result = JSON.parse(result);
           UpdateStudentList(result["result"]);
       }
    });
});