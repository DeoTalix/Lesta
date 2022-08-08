import os
print("BUILDING SHARED OBJECT")
os.system("python setup.py build_ext --inplace")
print()

print("STARTING TESTS")
os.system("python -m unittest tests")
print()