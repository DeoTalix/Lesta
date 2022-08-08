import cython
cimport libc.stdlib as stdlib

ctypedef long long int LL
  

cpdef quicksort(list numsequence):
    # The main function that calls quicksort implementation
    
    cdef LL pi, n = len(numsequence), i

    # Allocate memory for c array
    cdef LL* arr = <LL*>stdlib.malloc(cython.sizeof(LL) * n)

    if arr is NULL:
        raise MemoryError()

    # Copy values from numsequence to c array
    i = 0
    while i < n:
        arr[i] = numsequence[i]
        i += 1
        
    _quickSort(arr, 0, n - 1)

    # Copy values from c array back to numsequence
    i = 0
    while i < n:
        numsequence[i] = arr[i]
        i += 1
    
    # Free allocated memory
    stdlib.free(arr)
    
    
cdef void _quickSort(LL* arr, LL low, LL high):
    # The main function that implements quicksort
    # partitioning is inlined

    cdef LL pi, pivot, i, j, t    
    
    if (low < high):
        with nogil:
    
            pivot = arr[high]
            i = (low - 1)
            j = low   
        
            while (j <= high - 1): 
            
                if (arr[j] < pivot):
                 
                    i += 1
                    
                    #swap
                    t = arr[i]
                    arr[i] = arr[j]
                    arr[j] = t
                 
                j += 1
             
            # swap
            t = arr[i + 1]
            arr[i + 1] = arr[high]
            arr[high] = t 
            
            pi = (i + 1)

        _quickSort(arr, low, pi - 1)
        _quickSort(arr, pi + 1, high)
     