function filterModules() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("module_search");
    filter = input.value.toUpperCase();
    table = document.getElementById("modules_table");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function filterUsers() {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("users_search");
    filter = input.value.toUpperCase();
    table = document.getElementById("users_table");
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function createQuestions() {
    var table = $('.questions');
    var numOfQuestions = $('#number_of_questions').val();
    var currentChildren = table.children().length;
    var question = $('.qfields');

    for (var i = 0; i < (numOfQuestions - currentChildren); i++) {
        question.clone().insertAfter(question);
    }
}