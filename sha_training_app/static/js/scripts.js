function createFields() {
    var numberOfQuestions = document.getElementById('no_questions').value;
    var questionBase = document.getElementById('');

    for (var i = 0; i < numberOfQuestions; i++)
    {
    }
}


function search_user(value) {
    value = value.trim();
    if (value !== '') {
        $.ajax({
            url: 'search_users',
            data: {user: value},
            dataType: 'json',
            success: function (data) {
                var res = '';
                for (i in data.results) {
                    res += "<tr><td>data.results[i]['firstName']</td><td>{{ user.username }}</td><td>{{ user.email }}</td><td>{{ user.date_joined }}</td><td><a href='{{ url_for('admin.delete_user', user_id=user.id) }}' class='btn btn-danger'><i class='fa fa-trash'></i> Delete</a></td></tr>"
                }
            }
        })
    }
}