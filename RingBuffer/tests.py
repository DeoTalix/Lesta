import sys
if sys.version.startswith("2.7") != True:
    raise Exception(
        "This file has no support for python version ({}). Supported version is 2.7 only."
        .format(sys.version))

import unittest
from random import randint
from time import sleep
from ringbuff import RingBuffQueue, RingBuffList, RingBuffInvalidMaxsize, RingBuffIsEmpty, RingBuffOverflow


# TEST CASES FOR RING BUFF QUEUE

class RingBuffQueueGeneral(unittest.TestCase):
    def setUp(self):
        self.RingBuff = RingBuffQueue

    def test_raise_zero_maxsize(self):
        with self.assertRaises(RingBuffInvalidMaxsize):
            buff = self.RingBuff(maxsize=0)
    
    def test_raise_invalid_maxsize_type(self):
        with self.assertRaises(RingBuffInvalidMaxsize):
            buff = self.RingBuff(maxsize="2.5")

    def test_raise_isempty(self):
        buff = self.RingBuff(maxsize=4)
        with self.assertRaises(RingBuffIsEmpty):
            value = buff.get()

    def test_raise_isfull(self):
        buff = self.RingBuff(maxsize=1)
        buff.put("hello")
        with self.assertRaises(RingBuffOverflow):
            buff.put("world")

    def test_is_fifo(self):
        buff = self.RingBuff(maxsize=3)
        for i in range(3):
            buff.put(i)
        
        result = list(buff)
        self.assertEqual(result, [0, 1, 2])

    def test_is_overwritable(self):
        buff = self.RingBuff(maxsize=3, overwritable=True)
        for i in range(4):
            buff.put(i)

        result = list(buff)
        self.assertEqual(result, [1, 2, 3])


class RingBuffQueueThreading(unittest.TestCase):
    def setUp(self):
        self.RingBuff = RingBuffQueue
        self.run_setup()

    def run_setup(self):
        from threading import Thread, Lock

        c_get, c_inc = self.new_counter()
        self.limit = 300
        self.result = []

        buff = self.RingBuff(maxsize=4, overwritable=False)
        lock = Lock()

        t_list = []

        # Spawn 3 "putting" threads
        # and 2 "getting" threads
        for i in range(5):
            if i < 3:
                th = Thread(
                    target = self.thread_put,
                    args = (i, buff, lock, c_get, c_inc, self.limit))
            else:
                th = Thread(
                    target = self.thread_get,
                    args = (i, buff, lock, self.result, c_get, self.limit))
            t_list.append(th)

        for th in t_list:
            th.start()

        for th in t_list:
            th.join()

        for val in buff:
            self.result.append(self.process(val))


    def new_counter(self):
        """
        Closure function to store inner count.
        get() - gets current count only
        inc() - gets current count and increments it by one
        """
        d = {'count': 0}

        def get():
            return d['count']

        def inc():
            val = get()
            d['count'] += 1
            return val

        return get, inc


    def process(self, value):
        """
        Simulates value intensive processing.
        """
        n = randint(1, 10) / 100.
        sleep(n)
        return value


    def thread_put(self, id, buff, lock, c_get, c_inc, limit):
        """
        Fills buff with values obtained from c_inc until limit is reached.
        """

        with lock:
            i = c_inc()

        while True:
            with lock:
                try:
                    buff.put(i)
                    i = c_inc()
                except RingBuffOverflow:
                    pass

            if i >= self.limit:
                break
        return

    def thread_get(self, id, buff, lock, result, c_get, limit):
        """
        Gets values from buff. 
        Makes processing of those values. 
        Appends result of processing to result list.
        """
        while True:
            val = None

            with lock:
                try:
                    val = buff.get()
                except RingBuffIsEmpty:
                    pass

            if val != None:
                val = self.process(val)
                result.append(val)

            # This loop stops only if buff is empty
            # and the limit is reached
            if c_get() >= limit and buff.isempty:
                break
        return
        

    def test_length_hasnt_changed(self):
        self.assertEqual(self.limit, len(self.result))

    def test_no_duplicates(self):
        self.assertEqual(len(self.result), len(set(self.result)))




# TEST CASES FOR RING BUFF LIST

class RingBuffListGeneral(RingBuffQueueGeneral):
    def setUp(self):
        self.RingBuff = RingBuffList


class RingBuffListThreading(RingBuffQueueThreading):
    def setUp(self):
        self.RingBuff = RingBuffList
        self.run_setup()





if __name__ == '__main__':
    unittest.main()
