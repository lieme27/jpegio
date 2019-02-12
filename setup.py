# setup.py
from distutils.core import setup
from distutils.extension import Extension
#from setuptools import setup, find_packages
#from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize


import os
from os.path import join as pjoin
import sys
import glob

import numpy


cargs = []
#cargs.append("/DNPY_NO_DEPRECATED_API")

if sys.platform == 'win32': # Windows
    pass
else: # POSIX
    cargs.extend(['-O2', '-w', '-m64', '-fPIC',])
# end of if-else


DIR_ROOT = os.path.dirname(os.path.abspath(__file__))

DIR_LIBJPEG_HEADER = pjoin(DIR_ROOT, "jpegio", "libjpeg", "include")
DIR_LIBJPEG_SOURCE = pjoin(DIR_ROOT, "jpegio", "libjpeg", "src")

DIR_JPEGIO_HEADER = pjoin(DIR_ROOT, "jpegio")
DIR_JPEGIO_SOURCE = pjoin(DIR_ROOT, "jpegio")

incs = []
incs.append(DIR_LIBJPEG_HEADER)
incs.append(DIR_JPEGIO_HEADER)
incs.append(numpy.get_include())

srcs = []
for fpath in glob.glob(pjoin(DIR_LIBJPEG_SOURCE, "*.c")):
    print("[LIBJPEG]", fpath)
    srcs.append(fpath)
    
srcs.append(pjoin(DIR_JPEGIO_SOURCE, "decompressedjpeg.pyx"))
srcs.append(pjoin(DIR_JPEGIO_SOURCE, "read.c"))

print("include:", incs)
print("sources", srcs)

extensions = [
    Extension("decompressedjpeg",
              sources=srcs,
              language='c',
              include_dirs=incs,
              extra_compile_args=cargs)
]

dependency = ['cython>=0.x',
              'numpy>=0.12',]

file_formats = ['*.pxd', '*.pyx', '*.h', '*.c']
package_data = {
    'jpegio':file_formats,
    'jpegio/libjpeg':file_formats}

setup(name='jpegio',
      version='0.0.1',
      description='A library to to read and write the parameters of JPEG compression',
      url='http://github.com/dwgoon/jpegio',
      author='Daewon Lee',
      author_email='daewon4you@gmail.com',
      license='MIT',
      #packages=find_packages(),
      package_data=package_data,
      setup_requires=dependency,
      ext_modules=cythonize(extensions),
      cmdclass={'build_ext':build_ext},)
      #zip_safe=False) 

"""
# Extension of jpegio
incs_jpegio = []
incs_jpegio.append(numpy.get_include())
incs_jpegio.append(DIR_LIBJPEG_HEADER)

ext = cythonize(Extension("jpegio",
                          sources=['jpegio.pyx'],
                          language='c',
                          include_dirs=incs_jpegio,
                          extra_compile_args=cargs))
                          #extra_compile_args=cargs,
                          #extra_link_args=largs,
                          #library_dirs=lib_dirs,
                          #libraries=libs))         
setup(name='jpegio',
      ext_modules=ext,
      cmdclass={'build_ext':build_ext},) 

"""