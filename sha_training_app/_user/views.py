from . import user


@user.route('/')
def homepage():
    return """
    <h1>User Homepage</h1>
    """
