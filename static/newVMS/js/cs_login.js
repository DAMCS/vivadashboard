/**
 * Created by Deltatiger on 11/28/2016.
 * File for all login related AJAX / JS code
 */

$(document).ready(function(){
    /*
    $("#loginButton").on('click', function()  {
        var userid = $('#userid').val();
        var password = $('#password').val();
        $.post('/ajax/login/', {userid : userid, password : password}, function(response){
            var json_data = JSON.parse(response);
            if(json_data.status == 'success') {
                //Redirect the user
                window.location = "/index";
            } else {
                toastr.warning(json_data.msg);
            }
        });
    });
    */
    $('#loginActualForm').submit(function(e) {
        var userid = $('#userid').val();
        var password = $('#password').val();
        $.post('/ajax/login/', {userid : userid, password : password}, function(response){
            var json_data = JSON.parse(response);
            if(json_data.status == 'success') {
                //Redirect the user
                window.location = "/index";
            } else {
                toastr.warning(json_data.msg);
            }
        });
        e.preventDefault();
    });
});
