jinja_snippet = """
    { % for enrollment in current_user.account.enrollments %}
    { % if course.course_id == enrollment.course_id %}
    { % endif %}
    { % endfor %}
"""