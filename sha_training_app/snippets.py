jinja_snippet = """
    { % for enrollment in current_user.account.enrollments %}
    { % if course.course_id == enrollment.course_id %}
    { % endif %}
    { % endfor %}
"""

# When defining new relationships, put the foreign key before the relationship