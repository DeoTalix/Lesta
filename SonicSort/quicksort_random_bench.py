import sys, numpy as np
from random import randint
from time import perf_counter as perfc
import matplotlib.pyplot as plt
from multiprocessing import Process, Lock, Queue
from quicksort import quicksort



# Set this to False if you do not want multiprocessing
USEMP = True

if USEMP == False:

    # Dummy classes to turn off multiprocessing 
    # without too much writing
    class Process:
        def __init__(self, target=None, args=None):
            self.target = target
            self.args = args

        def start(self):
            self.target(*self.args)

        def join(self):
            pass

    class Lock:
        def __enter__(self, *args):
            return

        def __exit__(self, *args):
            return



def proc(name, e, r, lock=None, q1=None, q2=None):
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
        A = [randint(0, 10**e) for i in range(10**r)]
        
        A1 = np.array(A, dtype=np.int64)
        A2 = A.copy()

        t1 = perfc()
        quicksort(A1)
        T1 += perfc() - t1
        
        t2 = perfc()
        A2.sort()
        T2 += perfc() - t2

        # Finish process if arrays are not equal
        if list(A1) != A2:
            if lock is not None:
                lock.acquire()
            
            print("Arrays are not equal!")
            
            if lock is not None:
                lock.release()
            
            return

    if lock is not None:
        lock.acquire()
        
        if q1 is not None and q2 is not None:
            # As data is sent asynchronously
            # tuples are used in order to sort benchmarks by e value
            q1.put((e, T1 / 100))
            q2.put((e, T2 / 100))
    
    print(name, T1 / 100)
    print("timsort", T2 / 100)
    if T1 < T2:
        print(f"[+] {name} is {round(T2 / T1, 2)} times faster on range 0..10^{r} with rand ints from 0..10^{e}")
    else:
        print(f"[-] timsort is {round(T1 / T2, 2)} times faster on range 0..10^{r} with rand ints from 0..10^{e}")
    print()

    if lock is not None:
        lock.release()

    return



if __name__ == "__main__":

    lock = Lock()       # process lock
    p_list = []         # process list
    q1 = Queue()        # queue for quicklist benchmarks
    q2 = Queue()        # queue for timsort benchmarks
    T1 = []             # list for quicksort benchmarks
    T2 = []             # list for timsort benchmarks

    e = 1               # randint(0, 10**e)
    r = 4               # range(0, 10**r)


    # Collect processes
    while 10**e < sys.maxsize:
        p = Process(target=proc, args=("quicksort", e, r, lock, q1, q2))
        p_list.append(p)
        e += 1

    # Start processes
    for p in p_list:
        p.start()
            
    # Join processes
    for p in p_list:
        p.join()


    # Get data from the queues
    while (q1.empty() and q2.empty()) == False:

        if q1.empty() == False:
            T1.append(q1.get())
        
        if q2.empty() == False:
            T2.append(q2.get())


    # Close queues
    q1.close()
    q1.join_thread()
    q2.close()
    q2.join_thread()
    

    # Sort and split data
    T1.sort(key=lambda t: t[0])
    T2.sort(key=lambda t: t[0])
    
    E = [t[0] for t in T1]

    T1 = [t[1] for t in T1]
    T2 = [t[1] for t in T2]

    
    # Plot data
    plt.title("Quicksort vs Timsort | random integers")
    plt.plot(E, T1, color='r', label="quicksort")
    plt.plot(E, T2, color='g', label="timsort")
    plt.xlabel("rand int ranges (from 0 to 10**x)")
    plt.ylabel("averege performance (100 loops)")

    plt.show()
