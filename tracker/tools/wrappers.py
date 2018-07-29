

def print_args(function, *args, **kwargs):
        print("function", function.__name__)
        print("args", args)
        print("kwargs", kwargs)

class FunctionWrapper:

    @staticmethod
    def before_call(before_call_function):

        def wrapper(function):
            def inner_wrapper(*args, **kwargs):
                before_call_function(function, *args, **kwargs)
                return function(*args, **kwargs)
            return inner_wrapper

        return wrapper

    @staticmethod
    def wrap(before_call_function, after_call_function):

        def wrapper(function):
            def inner_wrapper(*args, **kwargs):
                before_call_function(function, *args, **kwargs)
                output =  function(*args, **kwargs)
                try:
                    return after_call_function(function, *output)
                except TypeError:
                    return after_call_function(function, output)[0]

            return inner_wrapper

        return wrapper

class ClassWrapper:

    ignored_methods = [
        '__dict__',
        '__class__',
        '__repr__',  # this has to be ignored otherwise the 'print' in wrapper keeps calling 'repr' recurisvely
        '__new__',  # gotta figure out why this needs to be ignored, dunno why it needs to be
    ]

    @staticmethod
    def wrap(function):
        """
        wraps every method in a class with a function
        """

        def class_wrapper(cls):
            """
            Class decorator that wraps a class with the wrap function
            """

            valid_methods = [x for x in dir(cls)
                if x not in ClassWrapper.ignored_methods
                ]
            for name in valid_methods:
                method = getattr(cls, name)
                setattr(cls, name, function(method))

            return cls

        return class_wrapper
