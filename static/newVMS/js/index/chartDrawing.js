/**
 * Required Parsing / Data set creation logics
 */
/**
 * Converts from RGB to hex color code for use in ChartJS
 */
function rgbToHex(red, green, blue) {
    return '#' + ('0' + parseInt(red).toString(16)).slice(-2) +
                 ('0' + parseInt(green).toString(16)).slice(-2) +
                 ('0' + parseInt(blue).toString(16)).slice(-2);
}

/**
 * Returns a number between 0 - 255
 */
function getRandomSingleColorValue() {
    return Math.floor(Math.random() * 255);
}

/**
 * Creates a list of random color combinations.
 */
function createRandomColors(numColors) {
    var colorList = [];
    for (var colorGenIter = 0; colorGenIter < numColors; colorGenIter++) {
        colorList.push(rgbToHex(getRandomSingleColorValue(), getRandomSingleColorValue(), getRandomSingleColorValue()));
    }
    return colorList;
}

/**
 * Vue objects for easy UI handling
 */
/**
 * Displays the tutor details in the Index Page
 */
var tutorSummaryVue = new Vue({
    el: '#tutorSummaryVueHolder',
    data: {
        tutors: []
    }
});
/**
 * Displays the faculty alloted for the students in the list
 */
var facultyAllotedListVue = new Vue({
    el: '#facultyAllotedListVue',
    data: {
        facultyList: []
    }
});
/**
 * Displays the list of company / organization and the # of people in said org.
 */
var studentCompanyDistVue = new Vue({
    el: '#studentCompanyDistVue',
    data: {
        companyCounts: []
    }
});

/**
 * Parses the JSON data to the required format (accepted by ChartJS).
 */
function parseGenericJSONData(jsonData) {
    if (jsonData === undefined) { return undefined; }
    var labels = [];
    var values = [];
    jsonData.forEach(entry => {
        labels.push(entry.label);
        values.push(entry.value);
    });
    var totalCount = labels.length;
    var colorList = createRandomColors(totalCount);
    return {
        labels: labels,
        datasets: [
            {
                data: values,
                backgroundColor: colorList
            }
        ]
    }
}

// Turning of legend display
Chart.defaults.global.legend.position = 'bottom';

$(document).ready(function(){
    /**
     * Pie chart representing the Distribution of the Students based on the Company.
     */
    $.ajax({
        url: '/ajax/student_company_graph',
        type: 'GET',
        error: function (err) {
            alert("Get Student Location Graph Ajax Error " + err.responseText);
        },
        success: function (data) {
            var jsonData = jQuery.parseJSON(data);
            studentCompanyDistVue.companyCounts = jsonData;
        }
    });
    $.ajax({
        url: '/ajax/student_location_graph',
        type: 'GET',
        error: function (err) {
            alert("Get Student Location Graph Ajax Error " + err.responseText);
        },
        success: function (data) {
            jsonData = jQuery.parseJSON(data);
            var canvas = document.getElementById('studentCityDistCanvas');
            var ctx = canvas.getContext('2d');
            var studentLocationDistChart = new Chart(ctx, {
                type: 'pie',
                data: parseGenericJSONData(jsonData),
                options: {
                    maintainAspectRatio: false
                }
            });
        }
    });
    $.ajax({
        url: '/ajax/index_student_report_status',
        type: 'GET',
        error: function (err) {
            alert("Get Student Report Submission Status Graph Ajax Error " + err.responseText);
        },
        success: function (data) {
            jsonData = jQuery.parseJSON(data);
            // Check the data
            if (!jsonData.status) {
                toastr.error(jsonData.message);
                return;
            }
            var canvas = document.getElementById('studentVivaAllotStatusCanvas');
            var ctx = canvas.getContext('2d');
            var studentLocationDistChart = new Chart(ctx, {
                type: 'pie',
                data: parseGenericJSONData(jsonData.payload),
                options: {
                    maintainAspectRatio: false
                }
            });
        }
    });
    // This is to fill the Tutor class details
    $.ajax({
        url: '/ajax/index_tutor_data',
        type: 'GET',
        error: function(err) {
            alert('Get Tutor Data AJAX Error : ' + err.responseText);
        },
        success: function(data) {
            var jsonData = JSON.parse(data);
            if (!jsonData.status) {
                alert(jsonData.msg);
                return;
            }
            // Give the data to Vue to render it.
            tutorSummaryVue.tutors = jsonData.data;
        }
    });
    // This is to fill the Guide Allotment details
    $.ajax({
        url: '/ajax/index_guide_data',
        type: 'GET',
        error: function(err) {
            alert('Get Guide Data AJAX Error : ' + err.responseText);
        },
        success: function(data) {
            var jsonData = JSON.parse(data);
            if (!jsonData.status) {
                alert(jsonData.msg);
                return;
            }
            facultyAllotedListVue.facultyList = jsonData.data;
        }
    });
});