#!/bin/ksh --login
set -x
date
cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/python
cp ./fg_t ./fg_blend_t.nc
cp ./fg ./fg_blend.nc
python da_blending_fv3.py
date

#sha1sum fg_blend*
diff -s fg_blend.nc fg
