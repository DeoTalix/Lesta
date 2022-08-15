#
cimport cython
cimport libc.stdlib as stdlib
from math import log
import numpy as np
cimport numpy as np


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cpdef void quicksort(Py_ssize_t[:] seq) except*:
    # The main function that calls quicksort implementation
    
    cdef:
        Py_ssize_t size = len(seq)
        int depth = round(log(size) * 2)

    np_quicksort(seq, depth)
    return

    
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef inline void np_quicksort(Py_ssize_t[:] seq, int depth) nogil:
    # The main function that implements quicksort
    # partitioning is inlined

    cdef: 
        Py_ssize_t i, j, low, high, pivot, part

    low = 0
    high = len(seq) - 1
    
    
    if (low < high):

        pivot = seq[high]
        i = (low - 1)
        j = low   
    
        while (j <= high - 1): 
            if (seq[j] < pivot):
                i += 1
                swap(seq, i, j)
            j += 1
            
        swap(seq, i + 1, high)
        
        part = (i + 1)

        if (high - low <= 64):
            insertionsort(seq[low : part])
            insertionsort(seq[part + 1 : high + 1])
            return

        elif (depth < 0):
            np_mergesort(seq[low : high + 1])
            return

        else:
            np_quicksort(seq[low : part], depth - 1)
            np_quicksort(seq[part + 1 : high + 1], depth - 1)

     
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef inline void swap(Py_ssize_t[:] seq, Py_ssize_t i, Py_ssize_t j) nogil:
    cdef Py_ssize_t t
    t = seq[i]
    seq[i] = seq[j]
    seq[j] = t
    return


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef void np_mergesort(Py_ssize_t[:] seq) nogil:
    cdef:
        Py_ssize_t size, left_size, right_size
        Py_ssize_t[:] left, right
        Py_ssize_t mid
        Py_ssize_t i, j, k

    size = len(seq)
        
    if size > 1:
        mid = size // 2

        left = seq[:mid]
        right = seq[mid:]

        if mid <= 128:
            insertionsort(left)
            insertionsort(right)
        else:
            np_mergesort(right)
            np_mergesort(left)

        seq[:] = merge(left, right)
    return


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef inline Py_ssize_t[:] merge(Py_ssize_t[:] left, Py_ssize_t[:] right) nogil:
    cdef:
        Py_ssize_t leftsize = len(left)
        Py_ssize_t rightsize = len(right)
        Py_ssize_t mergedsize = leftsize + rightsize
        Py_ssize_t[:] merged
        Py_ssize_t i, j, k

    if leftsize == 0:
        return right

    if rightsize == 0:
        return left

    with gil:
        merged = np.zeros(mergedsize, np.int64)

    i = 0
    j = 0
    k = 0

    while k < mergedsize:
        if left[i] <= right[j]:
            merged[k] = left[i]
            k += 1
            i += 1
        else:
            merged[k] = right[j]
            k += 1
            j += 1

        if j == rightsize:
            merged[k : k + leftsize - i] = left[i:]
            break

        if i == leftsize:
            merged[k : k + rightsize -j] = right[j:]
            break

    return merged


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef inline void insertionsort(Py_ssize_t[:] seq) nogil:
    cdef:
        Py_ssize_t i, j, pivot

    for i in range(1, len(seq)):
        pivot = seq[i]

        j = i - 1

        while j >= 0 and seq[j] > pivot:
            seq[j + 1] = seq[j]
            j -= 1

        seq[j + 1] = pivot


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef inline Py_ssize_t binsearch(Py_ssize_t[:] seq, 
                                 Py_ssize_t item,
                                 Py_ssize_t low, 
                                 Py_ssize_t high) nogil:
    cdef:
        Py_ssize_t mid = (low + high) // 2

    if (high <= low):
        return (low + 1) if (item > seq[low]) else low
  
    if (item == seq[mid]):
        return mid + 1
  
    # if (item > seq[mid]):
    #     return binsearch(seq, item, mid + 1, high)
    
    # return binsearch(seq, item, low, mid - 1)

    while low < high:
        mid = (low + high) // 2
        if seq[mid] < item:
            low = mid + 1
        else:
            high = mid - 1

    return (low + 1) if (item > seq[low]) else low

  
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
cdef inline void binsertionsort(Py_ssize_t[:] seq) nogil:
    cdef:
        Py_ssize_t size = len(seq)
        Py_ssize_t i, loc, j, k, selected
  
    for i in range(1, size):
    
        j = i - 1
        selected = seq[i]
  
        # find location where selected should be inseretd
        loc = binsearch(seq, selected, 0, j)
  
        # Move all elements after location to create space
        while (j >= loc):
        
            seq[j + 1] = seq[j]
            j -= 1
        
        seq[j + 1] = selected