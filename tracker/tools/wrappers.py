

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

def wrap_class(function):
    """
    wraps every method in a class with a function
    """

    def class_wrapper(cls):
        """
        Class decorator that wraps a class with the wrap function
        """
        ignored_methods = [
            '__dict__',
            '__class__',
            '__repr__',  # this has to be ignored otherwise the 'print' in wrapper keeps calling 'repr' recurisvely
            '__new__',  # gotta figure out why this needs to be ignored, dunno why it needs to be
        ]

        for name in [x for x in dir(cls) if x not in ignored_methods]:
            method = getattr(cls, name)
            setattr(cls, name, function(method))

        return cls

    return class_wrapper
