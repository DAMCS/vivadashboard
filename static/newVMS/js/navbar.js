
jQuery(document).ready(function ($) {

 var isFormMenuHidden=true
 var isIDFSent=parseInt($('#is_idf_sent').val(), 10);
 var isRSDFSent=parseInt($('#is_rsdf_sent').val(), 10);



 batch_mail = $("#batch_mail_id").val();
 $('#confirmation-popup').hide();
 $('#internship_details_form').hide();
 $('#report_submission_details_form').hide();
 $('#faculty_details_form').hide();
 $('#external_examiner_details_form').hide();
 var selectedFormName=""

	  $("#google-form-menu").on("click", function () {
	      if(isFormMenuHidden){
         $('#internship_details_form').delay( 5000 ).show();
         $('#report_submission_details_form').delay( 10000 ).show();
         $('#faculty_details_form').delay( 15000 ).show();
         $('#external_examiner_details_form').delay( 20000 ).show();
         isFormMenuHidden=false;
         }
         else{
          $('#internship_details_form').delay( 5000 ).hide();
         $('#report_submission_details_form').delay( 10000 ).hide();
         $('#faculty_details_form').delay( 15000 ).hide();
         $('#external_examiner_details_form').delay( 20000 ).hide();
         isFormMenuHidden=true;
         }
    });

    $("#internship_details_form").on("click", function () {
    if(isIDFSent)
          $('#confirmation-content').html('Do you want to send a reminder to fill the Internship Details Form to batch mail!!!');
          else
           $('#confirmation-content').html('Do you want to send the Internship Details Form to batch mail!!!');
         $('#confirmation-popup').show();
         selectedFormName="internship_details_form";
    });

     $("#report_submission_details_form").on("click", function () {
            if(isRSDFSent)
          $('#confirmation-content').html('Do you want to send a reminder to fill the Report Submission Details Form to batch mail!!!');
          else
           $('#confirmation-content').html('Do you want to send the Report Submission Details Form to batch mail!!!');
         $('#confirmation-popup').show();
          selectedFormName="report_submission_details_form";
    });

     $("#faculty_details_form").on("click", function () {
             $('#confirmation-content').html('Do you want to send the Faculty Details Form!!!');
         $('#confirmation-popup').show();
          selectedFormName="faculty_details_form";
    });

     $("#external_examiner_details_form").on("click", function () {
             $('#confirmation-content').html('Do you want to send the External Examiner Details Form!!!');
         $('#confirmation-popup').show();
          selectedFormName="external_examiner_details_form";
    });

$('#confirm-ok-google-form').on("click",function () {

        $('#confirmation-popup').hide();
        if(selectedFormName=="internship_details_form"){
            sendGoogleForm(selectedFormName,isIDFSent);
            isIDFSent=isIDFSent+1;
        }

        else if(selectedFormName=="report_submission_details_form"){
            sendGoogleForm(selectedFormName,isRSDFSent);
            isRSDFSent=isRSDFSent+1;
        }

    });

    $('#confirm-cancel-google-form').on("click",function () {
        $('#confirmation-popup').hide();
    });


});




function sendGoogleForm(selectedFormName,isReminder){
    console.log(selectedFormName)
     console.log(isReminder)
    $.ajax({
        url: '/ajax/send_google_form/',
        type: 'POST',
        dataType: 'json',
        data: {
            "form_name": selectedFormName,
            "is_reminder":isReminder
        },
        error: function (err) {
            alert("Send Mail Error " + err.responseText);
        },
        success: function (data) {
            //console.log(data);
            alert("Mail sent successfully");
        }
    });
}