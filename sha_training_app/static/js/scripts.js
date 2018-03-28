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

// function createQuestions() {
//     var table = $('.questions');
//     var numOfQuestions = $('#number_of_questions').val();
//     var currentChildren = table.children().length;
//     var question = $('.qfields');
//
//     var tr = document.createElement("tr");
//     // Create the question input
//     var questionTd = document.createElement("td");
//     var answerTd = document.createElement("td");
//
//     var questionInput = document.createElement("input");
//     var answerInput = document.createElement("input");
//
//     console.log(question.children());
//
//     for (var i = 0; i < (numOfQuestions - currentChildren); i++) {
//         questionInput.type = "text";
//         questionInput.name = "questions-" + i+1 + "-question";
//         questionInput.classList.add("form-control");
//         questionTd.appendChild(questionInput);
//
//         answerInput.type = "text";
//         answerInput.name = "questions-" + i+1 + "-question";
//         answerInput.classList.add("form-control");
//         answerTd.appendChild(answerInput);
//
//         tr.appendChild(questionTd);
//         tr.appendChild(answerTd);
//         tr.classList.add("qfields");
//
//         $(".qfields").insertAfter(".qfields");
//     }
// }

$(".add").on("click", function () {
    var currentCount = $('.questions').children().length;
    console.log("Current children: ", currentCount)
    var newCount = $('#number_of_questions').val()
    console.log("New children: ", newCount)
    if (newCount > currentCount) {
        for (var i = 0; i < (newCount - currentCount); i++) {
            var clone = $(".qfields")
                .clone(false, false)[0].innerHTML.replace(/(\d)/g, function (a) {
                return $('.questions').children().length
            });
            var newClone = "<tr>" + clone + "</tr>";
            $(newClone).appendTo(".questions");
        }
    } else {
        for (var i = currentCount; i > newCount; i--) {
            console.log("Removed element")
            $('.questions').remove($('.questions').lastChild)
        }
    }
    // console.log($(clone).attr("class"));
});

$(".edit_add").on("click", function () {
    console.log("Element being cloned ", clone);
    var currentCount = $('.questions').children().length;
    var newCount = $('#number_of_questions').val()
    for (var i = 0; i < (newCount - currentCount); i++) {
        var clone = $(".qfields")
            .clone(false, false)[0].innerHTML.replace(/(\d)/g, function (a) {
            return $('.questions').children().length
        });
        var newClone = "<tr>" + clone + "</tr>";
        $(newClone).appendTo(".questions");
    }
    // console.log($(clone).attr("class"));
});
