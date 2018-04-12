

import unittest
from tracker import TrackInt


class TestTrackInt(unittest.TestCase):

    def setUp(self):
        self.track_int = TrackInt(5)

    def tearDown(self):
        pass

    def test01_str(self):
        self.assertEqual(str(self.track_int), "5")

    def test01_is_int(self):
        self.assertTrue(self.track_int == 5)


    def test01_str(self):
        pass

    def test01_str(self):
        pass

if __name__ == "__main__":
    unittest.main()
