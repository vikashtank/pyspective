
import inspect

from ..tools.wrappers import ClassWrapper, FunctionWrapper


def track_variable(value):
    """
    takes a value and converts it into a Track Object

    args:
        value(obj): any Object

    returns:
        TrackObj: tracking object created by value
    """
    if isinstance(value, Track):
        return value
    elif isinstance(value, bool):
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


class FunctionTracker(FunctionWrapper):

    @staticmethod
    def track(function):

        def before_call(function, *args, **kwargs):
            #create action
            pass

        def after_call(function, *args):
            #create action
            return args

        return FunctionWrapper.wrap(before_call, after_call)(function)


class ClassTracker(ClassWrapper):

    @staticmethod
    def wrap(cls):
        """
        Decorator to replace all methods in a class by the parent method call
        and to return tracking class objects
        """

        def decorate(*args, **kwargs):
            """
            Decorator that gets the parent method, and wraps the return type
            """
            #get the parent of the class to be wrapped
            parent_type = cls.__bases__[0]
            parent_method = getattr(parent_type, name)
            return_value = parent_method(*args, **kwargs)
            return track_variable(return_value)

        return ClassWrapper.wrap(decorate)


class Track:
    pass


@ClassTracker.wrap
class TrackInt(int, Track):

    def __new__(cls, args):
        return super().__new__(cls, args)


@ClassTracker.wrap
class TrackStr(str, Track):

    def __new__(cls, args):
        return super().__new__(cls, args)


@ClassTracker.wrap
class TrackList(list, Track):

    def __new__(cls, args):
        return super().__new__(cls, args)
