/**
 * Created by Admin on 12/16/2016.
 */
//Page for the AJAX to get the config values
var _AJAX_CONFIG_PAGE = '/ajax/get_config/';
var _AJAX_CONFIG_SET_PAGE = '/ajax/set_configs/';

var _CreateCourseDOM = function(course_name) {
    /**
     * Creates a proper DOM structure using the name.
     */
    var data =  '<div class="config_course"><div class="config_course_name">';
    data += course_name;
    data += '</div><div class="config_course_close">';
    data += '<i class="fa fa-close"></i></div><div class="clearfix"></div></div>';
    return data;
};

var _AddCourseDOM = function(course_dom) {
    /**
     * Adds the HTML to the required DIV
     */
    var existing_data = $('#config_course_container').html();
    $('#config_course_container').html( existing_data + course_dom);
};

var _LoadCourses = function() {
    /**
     * Method for loading the courses into the DIV
     */
    $.ajax({
        url: '/ajax/get_course_list',
        type: 'GET',
        error: function (err) {
            alert("Get Course List Ajax Error " + err.responseText);
        },
        success: function (data) {
            data = jQuery.parseJSON(data);
            $.each(data.result,function(i,item){
                full_name = item.fields.course_name + " ( " + item.fields.short_name + " )";
                _AddCourseDOM(_CreateCourseDOM(full_name));
            });
        }
    });
};

/**
 * Configuration data of the currently selected.
 */
var _LoadConfigPageData = function(selected_page) {
    window.config_page_data_load_func[selected_page]();
};

/**
 * Used to store the data loaded settings.
 */
window.config_page_data_load_func = [];
window.config_pages = 3;

/**
 * Custom data loaders for each of the various pages
 */
window.config_page_data_load_func[0] = function() {
    $.post('/ajax/vms_session/', { action: 'get', session_year: '', session_sem: ''}, function(data) {
        var jsonData = JSON.parse(data);
        if (jsonData.result != 'none') {
            jsonData = JSON.parse(jsonData.result);
            $('#session_year').val(jsonData[0].fields.session_year);
            M.updateTextFields();
            if (jsonData[0].fields.session_sem == 'even') {
                $('#session_sem').val('even')
            } else {
                $('#session_sem').val('odd')
            }
        }
    });
};

window.config_page_data_load_func[1] = function() {
    //Loads the Table setting the Tutors
    $('#class-tutor-alloc-data').html('');
    $.ajax({
        url: '/ajax/get_course_list/',
        type: 'GET',
        success: function (data) {
            var jsonData = JSON.parse(data);
            window.current_tutor_table_contents = jsonData.result;
            $.each(jsonData.result, function (i, item) {
                var currentHtml = $('#class-tutor-alloc-data').html();
                var newHtml = '<tr>';
                newHtml += '<td>' + item.fields.course_name + '</td>';
                newHtml += '<td><input type="text" class="form-control" id="' + i + '_student_count"></td>';
                newHtml += '<td><input type="text" class="form-control" id="' + i + '_tutor"></td>';
                newHtml += '<td><input type="text" class="form-control" id="' + i + '_group_mail"></td>';
                $('#class-tutor-alloc-data').html(currentHtml + newHtml);
            });
            $.ajax({
                url: '/ajax/tutor_setup_config/',
                type: 'POST',
                data: {action: 'GET'},
                success: function(data) {
                    data = JSON.parse(data);
                    data_set = JSON.parse(data.result);
                    $.each(data_set,function(i,item) {
                        $('#' + i + "_student_count").val(item.fields.strength)
                        $('#' + i + "_tutor").val(item.fields.tutor)
                        $('#' + i + "_group_mail").val(item.fields.email_id)
                    });
                }
            });
        }
    });
}

/**
 * Loads the URL for the various Forms from the configuration
 */
window.config_page_data_load_func[3] = function() {
    // Get all three configurations
    get_config_promise('FacultyFormURL')
        .then(url => {
            $('#faculty_form_url').val(url);
            return get_config_promise('StudentFormURL');
        })
        .then(url => {
            $('#student_form_url').val(url);
            return get_config_promise('ReportFormURL');
        })
        .then(url => {
            $('#report_form_url').val(url);
            M.updateTextFields();
        })
        .catch(err => {
            toastr.error(err);
        });
};

$(document).ready(function(){
    window.config_tabs = $('ul.tabs').tabs();
    $('#session_sem').select();

    _LoadConfigPageData(0);
    $('#config_tabs_header li').on('click', function() {
        /**
         * Used for loading the data for the first time.
         */
        _LoadConfigPageData($(this).data('page'));
    });

    // START PAGE 1
    //Load the initial courses from the DB.
    _LoadCourses();

    $('#config_course_container').on('click', '.config_course_close', function(event) {
        /**
         * Deals with removing a course from the Course List
         */
        var course_to_remove = $(this).parent();
        var courseName = course_to_remove.text();
        //TODO Change it to the required format
        courseName = courseName.substr(0, courseName.indexOf(' ('));
        var course_dom = this;
        $.post('/ajax/course_modification/', {action: 'remove', course: courseName, shortName : '', degree:''}, function (data) {
            var jsonData = JSON.parse(data);
            if(jsonData.result == 'fail') {
                toastr.warn("Something went wrong. Try again.");
                return;
            }
            toastr.info("Course Removed");
            $(course_dom).parent().remove();
        });
    });

    $('#config_add_course').on('click', function(event){
        /**
         * Deals with the Add Course button in the First Config tab.
         */
        event.preventDefault();
        var course = $('#config_add_course_name').val();
        var courseShortName = $('#config_add_course_short_name').val();
        var degree = $('#config_add_degree').val();
        if(jQuery.trim(course).length <= 1) {
            toastr.error("Course name is too short.");
            return;
        }
        $.post('/ajax/course_modification/', { action: 'add', course: course, shortName : courseShortName,degree:degree}, function (data) {
            var jsonData = JSON.parse(data);
            if(jsonData.status == 'fail') {
                toastr.error('Error occurred. Try again.');
            } else {
                toastr.success('Course Added');
                full_course = course
                _AddCourseDOM(_CreateCourseDOM(full_course + ' ( ' + courseShortName + ' )'));
                $('#config_add_course_name').val('');
                $('#config_add_course_short_name').val('');
                $('#config_add_degree').val('');
            }
        });
    });

    $('#config_page_1_submit').on('click', function(){
        /**
         * Submits the contents of the first Configuration Page
         * Session_Year
         * Session_Sem
         */
        var session_year = $('#session_year').val();
        var session_sem = $('#session_sem').val();
        if(session_year == '' || session_sem == ''){
            toastr.error("Session year and semester must be entered . Try Again !");
            return;
        }
        $.post('/ajax/vms_session/',{action:'add',session_year:session_year,session_sem:session_sem},function(data){
            var jsonData = JSON.parse(data);
            console.log(jsonData)
            if(jsonData.result == 'success') {
                toastr.success("Configuration settings changed.");
            } else {
                toastr.error("Something went wrong. Try again.");
            }
        });

    });
    // END PAGE 1
    // START PAGE 2
    $('#config_page_2_submit').on('click', function () {
        var tbl = $('#config-2-table tr').get().map(function (row) {
            return $(row).find('td').get().map(function (cell) {
                if ($(cell).find('input').val() == null) {
                    return ($(cell).text());
                }
                return $(cell).find('input').val();
            });
        });
        tbl.shift();
        mydata = [];
        record = {}
        $.each(tbl, function (i, item) {
            record = {
                course: item[0],
                no_of_students: item[1],
                tutor: item[2],
                mail: item[3]
            }
            mydata.push(record);
        });
        final_data = JSON.stringify(mydata);
        $.ajax({
            url: '/ajax/tutor_setup_config/',
            type: 'POST',
            data: {
                action: 'SET',
                result: final_data
            },
            success: function (data) {
                data = JSON.parse(data)
                if (data.result == "success") {
                    toastr.success("Tutor Setup Saved ! ");
                } else {
                    toastr.error("Problem While saving ! ");
                }
            }
        });
    });
    // END PAGE 2
    // START PAGE 4
    $('#config_page_4_submit').on('click', function() {
        // Check if something is empty and confirm
        const studentFormURL = $('#student_form_url').val().trim();
        const facultyFormURL = $('#faculty_form_url').val().trim();
        const reportFormURL = $('#report_form_url').val().trim();
        if (studentFormURL === '' || facultyFormURL === '' || reportFormURL === '') {
            if (!confirm('Some of the URLs are empty. Do you want to proceed  with saving the data?')) {
                return;
            }
        }
        set_config_promise('FacultyFormURL', facultyFormURL)
            .then(status => {
                if (!status) {
                    return Promise.reject(status);
                }
                return set_config_promise('StudentFormURL', studentFormURL);
            })
            .then(status => {
                if (!status) {
                    return Promise.reject(status);
                }
                return set_config_promise('ReportFormURL', reportFormURL);
            })
            .then(status => {
                toastr.success('New URL values are saved.');
            })
            .catch(err => {
                console.log('Error occurred when setting the Form URLs.');
                console.log(err);
            });
    });
    // END PAGE 4
});