import unittest
from tracker.tools import wrappers


class TestBeforeCall(unittest.TestCase):

    def setUp(self):
        self.args = None
        self.kwargs = None

    def tearDown(self):
        pass

    def store_args(self, function, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def get_test_function(self):

        @wrappers.before_call(self.store_args)
        def add(a, b):
            return a + b

        return add

    def test_before_call_args(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(self.args, (5, 4))

    def test_before_call_result(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(result, 9)

    def test_before_call_kwargs(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(self.kwargs, {})



if __name__ == "__main__":
    unittest.main()
