

def print_args(function, *args, **kwargs):
        print("function", function.__name__)
        print("args", args)
        print("kwargs", kwargs)


def before_call(before_call_function):

    def wrapper(function):
        def inner_wrapper(*args, **kwargs):
            before_call_function(function, *args, **kwargs)
            return function(*args, **kwargs)
        return inner_wrapper

    return wrapper
