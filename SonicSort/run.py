import os
print("BUILDING SHARED OBJECT")
os.system("python quicksort_setup.py build_ext --inplace")
print()

print("STARTING TESTS")
os.system("python quicksort_tests.py")
print()

print("STARTING BENCHMARKS")
os.system("python quicksort_random_bench.py")
print()