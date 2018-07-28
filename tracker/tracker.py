import inspect
from .tools.wrappers import before_call, print_args

def wrap_function(function):
    """
    Decorating function that wraps a function and prints its arguments before executing
    """
    def wrapper(*args, **kwargs):
        print("name", function.__name__)
        print("args", args)
        print("kwargs", kwargs)
        return function(*args, **kwargs)
    return wrapper


def wrap_class(cls):
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
        setattr(cls, name, wrap_function(method))

    return cls


def track_wrap(cls):
    """
    Decorator to replace all methods in a class by the parent method call
    and to return tracking class objects
    """

    def get_super(name):
        """
        function that gets the parent method with the same name and decorates it

        args:
            name(str): name of the method to find in the parent
        """

        def choose_return_type(value):
            """
            takes a value and converts it into a Track Object

            args:
                value(obj): any Object

            returns:
                TrackObj: tracking object created by value
            """
            if isinstance(value, bool):
                return value
            elif isinstance(value, int):
                return TrackInt(value)
            elif isinstance(value, str):
                return TrackStr(value)
            elif isinstance(value, list):
                new_list = []
                for index, each_value in enumerate(value):
                    new_list.append(choose_return_type(each_value))
                return TrackList(new_list)
            else:
                raise ValueError("unknown return type: {0}".format(type(value)))


        def decorate(*args, **kwargs):
            """
            Decorator that gets the parent method, and wraps the return type
            """
            #get the parent of the class to be wrapped
            parent_type = cls.__bases__[0]
            parent_method = getattr(parent_type, name)
            if False:
                pass
            else:
                return_value = parent_method(*args, **kwargs)
                return choose_return_type(return_value)

        return decorate

    ignored_methods = [
        '__dict__',
        '__bool__'
        '__init__',
        '__class__',
        '__repr__',  # this has to be ignored otherwise the 'print' in wrapper keeps calling 'repr' recurisvely
        '__new__',  # gotta figure out why this needs to be ignored, dunno why it needs to be
    ]



    for name in [x for x in dir(cls) if x not in ignored_methods]:
        method = getattr(cls, name)
        setattr(cls, name, get_super(name))

    return cls


@track_wrap
class TrackInt(int):

    def __new__(cls, args):
        return super().__new__(cls, args)


@track_wrap
class TrackStr(str):

    def __new__(cls, args):
        return super().__new__(cls, args)


@track_wrap
class TrackList(list):

    def __new__(cls, args):
        return super().__new__(cls, args)


@wrap_class
class test_class(object):

    def __init__(self, a):
        self.a = a

    def add_two(self):
        return self.a+2


if __name__ == "__main__":
    a = test_class(5)

    a.add_two()
