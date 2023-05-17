#!/bin/bash -l

#f2py3.8 --build-dir . -c -m remap remap.f90
#f2py3.8 -DF2PY_REPORT_ATEXIT --build-dir . -c -m remap remap.f90

f2py3.8 -DF2PY_REPORT_ATEXIT --build-dir . -c --f90flags='-fopenmp' -L/pe/intel/compilers_and_libraries_2020.4.304/linux/compiler/lib/intel64_lin/libiomp5.so -liomp5 -m remap remap.f90
