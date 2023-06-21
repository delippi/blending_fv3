#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/step1.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/step1.err
##PBS -l select=1:ncpus=1
#PBS -l select=2:ncpus=128
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:45:00

ulimit -s unlimited
export OMP_STACKSIZE=2G
export OMP_NUM_THREADS="96"  #largest value tried that doesn't crash with fastest time = 96 (68s)
                             # 96 1G (102s)
                             # 96 2G ( 82s)
                             # 96 3G ( 92s)
                             # 96 4G ( 90s)

                             #old stats:
                             # 32 (75s)
                             # 96 (34s)
                             #128 (41s)
                             #256 (84s)
export FI_OFI_RXM_SAR_LIMIT=3145728
export FI_MR_CACHE_MAX_COUNT=0
export MPICH_OFI_STARTUP_CONNECT=1

echo "OMP_STACKSIZE="$OMP_STACKSIZE
echo "OMP_NUM_THREADS="$OMP_NUM_THREADS


cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds


echo -ne "Copying files..............\r"
# GDAS FILES
cp ./coldstart/out.atm.tile1.nc ./out.atm.tile1.nc
cp ./coldstart/gfs_ctrl.nc ./gfs_ctrl.nc

# WARMSTART FILES
cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_core.res.nc ./fv_core.res.nc
cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_core.res.tile1.nc ./fv_core.res.tile1.nc
cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_tracer.res.tile1.nc ./fv_tracer.res.tile1.nc

# FIX FILES
cp /lfs/h2/emc/global/noscrub/emc.global/FIX/fix/orog/20220805/C768/C768_grid.tile1.nc .
cp /lfs/h2/emc/global/noscrub/emc.global/FIX/fix/orog/20220805/C768/C768_oro_data.tile1.nc .
echo "Copying files.............. Done."

warm=./fv_core.res.tile1.nc
cold=./out.atm.tile1.nc
grid=./C768_grid.tile1.nc
akbk=./fv_core.res.nc
akbkcold=./gfs_ctrl.nc
orog=./C768_oro_data.tile1.nc

python da_chgres_winds.py $warm $cold $grid $akbk $akbkcold $orog 

echo -ne "Starting comparison script...\r"
bash ./compare_results.sh
echo "Starting comparison script... Done."
