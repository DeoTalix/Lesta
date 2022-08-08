import unittest, sys
from random import randint
from time import perf_counter as perfc
from quicksort import quicksort


class QuicksortGeneral(unittest.TestCase):
    def setUp(self):
        self.sortfunc = quicksort
        self.arr = [randint(0, sys.maxsize) for i in range(10**6)]

    def tearDown(self):
        self.arr = None

    def test_can_handle_sysmaxsize(self):
        arr1 = self.arr.copy()
        arr1.sort()

        arr2 = self.arr.copy()
        self.sortfunc(arr2)
        
        self.assertEqual(arr1, arr2)

    def test_faster_than_timsort(self):
        arr1 = self.arr.copy()
        arr2 = self.arr.copy()

        t = perfc()
        arr1.sort()
        t1 = perfc() - t

        t = perfc()
        self.sortfunc(arr2)
        t2 = perfc() - t

        self.assertLess(t2, t1)



if __name__ == "__main__":

    unittest.main()