// Some constants that will come in handy
const VIEW_DISPLAY_MODE = 'View';
const EDIT_DISPLAY_MODE = 'Edit';

window.guideSelectVue = new Vue({
    el: '#vue_guide_select_app',
    data: {
        // List of all faculties
        facultyList: [],
        // Current mode of display
        currentDisplayMode: VIEW_DISPLAY_MODE,
        // Recommended count for the guides.
        recommendedCount: 0
    },
    methods: {
        /**
         * Changes the state of the view.
         */
        changeState: function() {
            if (this.currentDisplayMode == EDIT_DISPLAY_MODE) {
                // Save the data
                saveGuideList().then(processStatus => {
                    this.currentDisplayMode = VIEW_DISPLAY_MODE;
                });
            } else {
                // Here we do not require much work. Go ahead and just change the data.
                this.currentDisplayMode = EDIT_DISPLAY_MODE;
            }
        },
        printData: function() {
            console.log(this.facultyList);
        }
    },
    created: function() { // This is a lifecycle hook for fun
        console.log('Yay created');
    },
    computed: {
        filteredFacultyList: function() {
            if (this.currentDisplayMode == EDIT_DISPLAY_MODE) {
                return this.facultyList;
            } else {
                return this.facultyList.filter(function(facultyData) {
                    return facultyData !== undefined && facultyData.is_guide;
                });
            }
        }
    }
});

/**
 * Updates the global DS using the given result.
 * @param {Object} result JSON response from the AJAX call to the  Server
 */
function parseResultsAndUpdateDS(result) {
    window.guideSelectVue.recommendedCount = result['rc'];
    window.guideSelectVue.facultyList = result['result'].map((facultyModelObj) => {
        if (facultyModelObj !== undefined) {
            // First convert the is_guide field to a boolean value.
            facultyModelObj['fields']['is_guide'] = (facultyModelObj['fields']['is_guide'] == '1');
            facultyModelObj['fields'].pk = facultyModelObj['pk'];
            return facultyModelObj['fields'];
        } else {
            return {};
        }
    });
}

/**
 * Refreshes the data displayed in the Grid
 * @return {Promise<boolean>}
 */
function refreshFacultyList() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "POST",
            url: "/ajax/get_faculty_list/",
            dataType: "json",
            success: function(result) {
                parseResultsAndUpdateDS(result);
                resolve(true);
            },
            error: reject
        });
    });
}

/**
 * Saves the current list of guides
 * @return {Promise<boolean>} Promise with the status of the update process
 */
function saveGuideList() {
    const newGuideList = window.guideSelectVue.facultyList.filter(faculty => faculty.is_guide).map(faculty => faculty.pk);
    return new Promise((resolve, reject) => {
        $.ajax({
            type:"POST",
            url:"/ajax/update_guides/",
            data: {
                "input[]": newGuideList
            },
            dataType: "json",
            success: function(result) {
                parseResultsAndUpdateDS(result);
                resolve(true);
            },
            error: reject
        });
    });
}



// Send the AJAX Request to get the Guide List
$(document).ready(function() {
    refreshFacultyList();
});