#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/test_chgres_winds/blending.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/test_chgres_winds/blending.err
#PBS -l select=2:ncpus=128
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:30:00

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds

cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_core.res.nc ./fv_core.res.nc
cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_core.res.tile1.nc ./fv_core.res.tile1.nc
cp ./coldstart/out.atm.tile1.nc ./out.atm.tile1.nc

python ./da_chgres_winds.py ./fv_core.res.tile1.nc ./out.atm.tile1.nc ./fv_core.res.nc
