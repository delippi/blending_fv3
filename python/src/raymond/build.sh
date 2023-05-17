#!/bin/bash

#f2py3.9 --build-dir . -c raymond.f -m raymond -DF2PY_REPORT_ON_ARRAY_COPY=1
#f2py3.9 --build-dir . -c -m raymond raymond.f -DF2PY_REPORT_ON_ARRAY_COPY=1
#f2py --build-dir . -c -m raymond raymond.f
#conda activate
#f2py3.9 --build-dir . -c -m raymond raymond.f
#f2py3.9 --build-dir . -c -m balance balance.f90
#f2py --build-dir . -c -m balance balance.f90

#source /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/env/build_wcoss2_intel.env
f2py3.8 --build-dir . -c -m raymond raymond.f
