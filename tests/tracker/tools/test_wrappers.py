import unittest
from tracker.tools.wrappers import FunctionWrapper, ClassWrapper


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

        @FunctionWrapper.before_call(self.store_args)
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

class TestFunctionWrap(unittest.TestCase):

    def setUp(self):
        self.in_args = None
        self.out_args = None
        self.in_kwargs = None

    def tearDown(self):
        pass

    def store_args(self, function, *args, **kwargs):
        self.in_args = args
        self.in_kwargs = kwargs

    def store_output(self, function, *args):
        self.out_args = args
        return args

    def get_test_function(self):
        @FunctionWrapper.wrap(self.store_args, self.store_output)
        def add(a, b):
            return a + b

        return add

    def get_test_function_multi_output(self):
        @FunctionWrapper.wrap(self.store_args, self.store_output)
        def add(a, b):
            return a, b

        return add

    def test_before_call_in_args(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(self.in_args, (5, 4))

    def test_before_call_result(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(result, 9)

    def test_before_call_in_kwargs(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(self.in_kwargs, {})

    def test_after_call_output(self):
        result = self.get_test_function()(5, 4)
        self.assertEqual(self.out_args[0], 9)

    def test_after_call_multi_output(self):
        result = self.get_test_function_multi_output()(5, 4)
        self.assertEqual(self.out_args, (5, 4))

    def test_after_call_multi_result(self):
        result = self.get_test_function_multi_output()(5, 4)
        self.assertEqual(self.out_args, (5, 4))

class TestWrapClass(unittest.TestCase):

    def setUp(self):
        self.results = {}

    def tearDown(self):
        pass

    def store_args(self, function, *args, **kwargs):
        self.results[function.__name__] = {'args': args, 'kwargs':kwargs}

    def get_wrapped_class(self, a, b):

        @ClassWrapper.wrap(FunctionWrapper.before_call(self.store_args))
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
