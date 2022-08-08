import sys
from random import randint
from quicksort import quicksort
from time import perf_counter as perfc

def avg_perf(name, func, n, lock):
    total_t = 0

    for i in range(n):
        arr1 = [randint(0, sys.maxsize) for i in range(10**4)]
        arr2 = arr1.copy()
        arr2.sort()

        t = perfc()
        func(arr1)
        total_t += perfc() - t
        if arr1 != arr2:
            raise Exception("Sorted arrays do not match")

    with lock:
        print(name)
        print(total_t / n)
        print("Sorted arrays do match is", arr1 == arr2)
        print()


def main():
    from multiprocessing import Process, Lock

    lock = Lock()

    n = 100

    t1 = Process(
        target = avg_perf, 
        args = ("timsort", lambda a: a.sort(), n, lock)
    )
    
    t2 = Process(
        target = avg_perf, 
        args = ("quicksort", lambda a: quicksort(a), n, lock)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()