from functools import wraps


def log_error(func):
    """A decorator which prints any occuring error."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e, end="\n")

    return decorated_function
