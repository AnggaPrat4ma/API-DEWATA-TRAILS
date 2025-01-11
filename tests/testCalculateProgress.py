import unittest
from helper.functionsCalculateProgress import calculate_progress_percentage

class TestCalculateProgressPercentage(unittest.TestCase):
    def setUp(self):
        print("\nStarting a new test case...")

    def tearDown(self):
        print("Test case finished\n")

    def test_target_zero(self):
        # Target jumlah donor adalah 0, maka progress harus 0%
        self.assertEqual(calculate_progress_percentage(50, 0), 0.0)

    def test_approved_donors_zero(self):
        # Jumlah donor disetujui adalah 0, dan target jumlah donor adalah 100
        self.assertEqual(calculate_progress_percentage(0, 100), 0.0)

    def test_progress_halfway(self):
        # Jumlah donor yang disetujui adalah setengah dari target jumlah donor
        self.assertEqual(calculate_progress_percentage(50, 100), 50.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)