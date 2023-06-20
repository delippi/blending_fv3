#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test/blending.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test/blending.err
#PBS -l select=2:ncpus=128
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:45:00

ulimit -s unlimited
export OMP_STACKSIZE=2G
export OMP_NUM_THREADS="52"  #largest value tried that doesn't crash with fastest time =  (s)
                             #1
                             #2
                             #4
                             #13
                             #26
                             #52
                             #364
export FI_OFI_RXM_SAR_LIMIT=3145728
export FI_MR_CACHE_MAX_COUNT=0
export MPICH_OFI_STARTUP_CONNECT=1

echo "OMP_STACKSIZE="$OMP_STACKSIZE
echo "OMP_NUM_THREADS="$OMP_NUM_THREADS


cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/tmp_ICS

echo -ne "Copying files..............\r"
# GDAS FILES
cp ./gdas/out.atm.tile7.nc ./out.atm.tile7.nc
cp ./gdas/gfs_ctrl.nc      ./gfs_ctrl.nc
cp ./gdas/gfs.bndy.nc      ./gfs.bndy.nc

# RRFS FILES
cp ./rrfs/RESTART/20220720.180000.fv_core.res.tile1.nc   ./fv_core.res.tile1.nc
#cp ./rrfs/RESTART/20220720.180000.fv_tracer.res.tile1.nc ./fv_tracer.res.tile1.nc
cp ./rrfs/RESTART/20220720.180000.fv_core.res.nc         ./fv_core.res.nc

# FIX FILES
halo=".halo4"
halo=""
FIX_DIR=/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/regional_workflow/fix/lam/RRFS_CONUS_3km/
cp $FIX_DIR/C3359_grid.tile7${halo}.nc     ./C3359_grid.tile7${halo}.nc
cp $FIX_DIR/C3359_oro_data.tile7${halo}.nc ./C3359_oro_data.tile7${halo}.nc
echo "Copying files.............. Done."

warm=./fv_core.res.tile1.nc
cold=./out.atm.tile7.nc
grid=./C3359_grid.tile7${halo}.nc
akbk=./fv_core.res.nc
akbkcold=./gfs_ctrl.nc
orog=./C3359_oro_data.tile7${halo}.nc
bndy=./gfs.bndy.nc

python da_chgres_winds.py $warm $cold $grid $akbk $akbkcold $orog $bndy


