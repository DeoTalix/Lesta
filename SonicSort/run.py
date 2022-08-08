import os
print("BUILDING SHARED OBJECT")
os.system("python setup.py build_ext --inplace")
print()

print("STARTING TESTS")
os.system("python tests.py")
print()

print("STARTING BENCHMARKS")
os.system("python bench.py")
print()