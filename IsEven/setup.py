from distutils.core import setup
from Cython.Build import cythonize

module = cythonize("iseven.pyx", language_level='3')
setup(ext_modules = module)