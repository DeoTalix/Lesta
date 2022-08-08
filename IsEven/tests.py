import unittest, sys
from random import randint
from time import perf_counter as perfc
from iseven import iseven


class IsEvenGeneral(unittest.TestCase):
    def test_bad_input(self):
        with self.assertRaises(TypeError):
            iseven("hello")

    def test_can_handle_sysmaxsize(self):
        result = int(sys.maxsize & 1 == 0)
        self.assertEqual(iseven(sys.maxsize), result)

    def test_faster_than_native(self):
        n = 1000
        result = None

        total_t = 0
        for i in range(n):
            t = perfc()
            result = int(sys.maxsize & 1 == 0)
            total_t += perfc() - t
        T1 = total_t / n

        total_t = 0
        for i in range(n):
            t = perfc()
            resutl = iseven(sys.maxsize)
            total_t += perfc() - t
        T2 = total_t / n

        self.assertLess(T2, T1)
        



if __name__ == "__main__":

    unittest.main()