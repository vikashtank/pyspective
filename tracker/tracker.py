from .type_trackers import track_variable
from .tools.wrappers import FunctionWrapper

class Tracker:

    @staticmethod
    def track(function):


        # transform inputs to track variables, if required

        # create action
        # run function and get outputs
        # convert outputs if necessary
        # return converted outputs


        return function


@Tracker.track
def main(a, b, c):
    return a + b + c


if __name__ == "__main__":
    main(2, 3, 4)
