from itertools import cycle
import unittest, sys
from random import randint
from time import perf_counter as perfc
import numpy as np
from quicksort import quicksort


class QuicksortGeneral(unittest.TestCase):
    leo_nums = None

    def setUp(self):
        self.sortfunc = quicksort

    def tearDown(self):
        self.arr = None

    def preprocess(self, arr):
        return np.array(arr, dtype=np.int64)

    def postprocess(self, arr):
        return list(arr)

    def cycle(self, generate_sequence):
        """
        Process that generates benchmarks.
        A is list (of size 10**r) with random numbers (from 0 to 10**e) in it.
        T1, T2 - quicksort, timsort average sorting time.
        Benchmarks are put in the queues q1, q2 when looping is finished.
        Finally, information is printed out.
        """
        
        T1 = 0
        T2 = 0

        for i in range(100):
            A = generate_sequence()
            
            A1 = self.preprocess(A)
            A2 = A.copy()

            t1 = perfc()
            quicksort(A1)
            T1 += perfc() - t1
            
            t2 = perfc()
            A2.sort()
            T2 += perfc() - t2

            # Finish process if arrays are not equal
            if self.postprocess(A1) != A2:               
                raise Exception("Arrays are not equal!")
        
        return (T1 / 100, T2 / 100)

    def test_can_handle_int_of_any_size(self):
        n = 10
        arr1 = [sys.maxsize for i in range(n)]
        arr1.sort()

        arr2 = self.preprocess(arr1)
        self.sortfunc(arr2)
        arr2 = self.postprocess(arr2)

        self.assertEqual(arr1, arr2)

    # def test_faster_than_timsort_on_sorted(self):
    #     n = 10**4
    #     t1, t2 = self.cycle(lambda: [i for i in range(n)])
    #     self.assertLess(t1, t2)

    # def test_faster_than_timsort_on_almost_sorted(self):
    #     n = 10**4
    #     def generate_sequence():
    #         arr = [i for i in range(1, n)]
    #         arr[0], arr[-1] = arr[-1], arr[0]
    #         return arr

    #     t1, t2 = self.cycle(generate_sequence)
    #     self.assertLess(t1, t2)

    def test_faster_than_timsort_on_mangled(self):
        n = 10**4
        
        def generate_sequence():
            arr = [i for i in range(1, n)]
            for i in range(1, len(arr), 2):
                arr[i], arr[i-1] = arr[i-1], arr[i]
            return arr
        
        t1, t2 = self.cycle(generate_sequence)
        self.assertLess(t2, t1)

    def test_faster_than_timsort_on_random(self):
        n = 10**4
        t1, t2 = self.cycle(lambda: [randint(0, sys.maxsize) for i in range(n)])
        self.assertLess(t1, t2)



if __name__ == "__main__":

    unittest.main()
