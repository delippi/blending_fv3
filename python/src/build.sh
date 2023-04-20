#!/bin/bash

#f2py3.9 --build-dir . -c raymond.f -m raymond -DF2PY_REPORT_ON_ARRAY_COPY=1
#f2py3.9 --build-dir . -c -m raymond raymond.f -DF2PY_REPORT_ON_ARRAY_COPY=1

conda activate
f2py3.9 --build-dir . -c -m raymond raymond.f
f2py3.9 --build-dir . -c -m balance balance.f90
