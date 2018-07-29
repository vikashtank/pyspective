import unittest
from tracker.type_trackers import TrackInt
from tracker import Tracker


class TestTrackerSimpleMethod(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_simple_method(self):

        @Tracker.track
        def simple_method(a, b, c):
            return a + b + c

        return simple_method

    def test_result_value(self):
        result = self.get_simple_method()(3, 4, 5)
        self.assertEqual(result, 12)

    def _test_result_type(self):
        result = self.get_simple_method()(3, 4, 5)
        self.assertIsInstance(result, type(TrackInt))

    def _test_log_length(self):
        self.get_simple_method()(3, 4, 5)
        self.assertEqual(len(Tracker.log), 2)


if __name__ == "__main__":
    unittest.main()
