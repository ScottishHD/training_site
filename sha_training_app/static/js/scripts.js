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

function filterModules() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("module_search");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
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