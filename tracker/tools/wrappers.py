

def print_wrapper(function):
    """
    Decorating function that wraps a function and prints its arguments before executing
    """
    def wrapper(*args, **kwargs):
        print("name", function.__name__)
        print("args", args)
        print("kwargs", kwargs)
        return function(*args, **kwargs)
    return wrapper


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


@before_call(print_args)
def test_function(a, b):
    return a + b

if __name__ == '__main__':
    test_function(5, 6)
