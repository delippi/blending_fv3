#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test/blending.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test/blending.err
#PBS -l select=2:ncpus=128
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:10:00

set -x
cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test
cp ./gdas/out.atm.tile7.nc .
# Copy the RRFS restarts because they are overwritten
cp ./rrfs/RESTART/20220720.180000.fv_core.res.tile1.nc ./fv_core.res.tile1.nc
cp ./rrfs/RESTART/20220720.180000.fv_tracer.res.tile1.nc ./fv_tracer.res.tile1.nc
cp ./rrfs/RESTART/20220720.180000.fv_core.res.nc ./fv_core.res.nc

# Does not remap chgres winds to D-grid (blends u and u_s, which is not correct)
#python ./da_blending_fv3.py out.atm.tile7.nc 20220720.180000.fv_core.res.tile1.nc 20220720.180000.fv_tracer.res.tile1.nc

# Does remap chgres winds to D-grid
python ./da_blending_fv3_dgrid.py out.atm.tile7.nc fv_core.res.tile1.nc fv_tracer.res.tile1.nc fv_core.res.nc

#icsdir=./rrfs/INPUT
#mkdir -p $icsdir
#cp gfs_ctrl.nc $icsdir/.
#mv 20220720.180000.fv_core.res.tile1.nc   $icsdir/fv_core.res.tile1.nc
#mv 20220720.180000.fv_tracer.res.tile1.nc $icsdir/fv_tracer.res.tile1.nc
