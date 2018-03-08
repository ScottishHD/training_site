from . import user

@user.route('/')
def user_home():
    return """
    <h1>User Homepage</h1>
    """