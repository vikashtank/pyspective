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

class TestWrapClass(unittest.TestCase):

    def setUp(self):
        self.results = {}

    def tearDown(self):
        pass

    def store_args(self, function, *args, **kwargs):
        self.results[function.__name__] = {'args': args, 'kwargs':kwargs}

    def get_wrapped_class(self, a, b):

        @wrappers.ClassWrapper.wrap(wrappers.before_call(self.store_args))
        class Dummy:

            def __init__(self, a, b):
                self.a = a
                self.b = b

            def add(self):
                return self.a + self.b

        return Dummy(a, b)

    def test_wrap_class_constructor_args(self):
        dummy = self.get_wrapped_class(3, 4)
        self.assertEqual(self.results['__init__']['args'], (dummy, 3, 4))

    def test_wrap_class_constructor_kwargs(self):
        dummy = self.get_wrapped_class(3, 4)
        self.assertEqual(self.results['__init__']['kwargs'], {})

    def test_wrap_class_no_method_in_resuts_before_run(self):
        dummy = self.get_wrapped_class(3, 4)
        self.assertFalse( 'add' in self.results)

    def test_wrap_class_method_args(self):
        dummy = self.get_wrapped_class(3, 4)
        dummy.add()
        self.assertEqual(self.results['add']['args'][0], dummy)

    def test_wrap_class_method_kwargs(self):
        dummy = self.get_wrapped_class(3, 4)
        dummy.add()
        self.assertEqual(self.results['add']['kwargs'], {})


























if __name__ == "__main__":
    unittest.main()
