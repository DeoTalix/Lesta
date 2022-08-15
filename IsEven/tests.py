import unittest, sys
from random import randint
from time import perf_counter as perfc
from math import fmod
from iseven import iseven


class IsEvenGeneral(unittest.TestCase):
    def setUp(self) -> None:
        self.iseven = iseven
        self.fmod_iseven = lambda n: fmod(n, 2) == 0
        self.band_iseven = lambda n: n & 1 == 0

    def speed_bench(self, func):
        n = 1000

        total_t1 = 0
        total_t2 = 0
        for _ in range(n):
            num = randint(0, sys.maxsize)

            t = perfc()
            result = func(num)
            total_t1 += perfc() - t

            t = perfc()
            result = iseven(num)
            total_t2 += perfc() - t

        T1 = total_t1 / n
        T2 = total_t2 / n
        return T1, T2

    def test_is_even(self):
        self.assertEqual(iseven(2), True)

    def test_is_odd(self):
        self.assertEqual(self.iseven(3), False)

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            iseven("hello")

    def test_can_handle_sysmaxsize(self):
        result = int(sys.maxsize & 1 == 0)
        self.assertEqual(iseven(sys.maxsize), result)

    def test_faster_than_native(self):
        T1, T2 = self.speed_bench(self.band_iseven)
        self.assertLess(T2, T1)

    def test_faster_than_fmod(self):
        T1, T2 = self.speed_bench(self.fmod_iseven)
        self.assertLess(T2, T1)

        



if __name__ == "__main__":

    unittest.main()