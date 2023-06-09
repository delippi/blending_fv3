#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/step1.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/step1.err
#PBS -l select=2:ncpus=128
##PBS -l select=1:ncpus=1
##PBS -l pmem=2gb
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:45:00

ulimit -s unlimited
export OMP_STACKSIZE=1G
export OMP_NUM_THREADS="96"  #largest value tried that doesn't crash with fastest time = 96 (34s)
                             # 32 (75s)
                             # 96 (34s)
                             #128 (41s)
                             #256 (84s)
export FI_OFI_RXM_SAR_LIMIT=3145728
export FI_MR_CACHE_MAX_COUNT=0
export MPICH_OFI_STARTUP_CONNECT=1

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds

#cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_core.res.nc ./fv_core.res.nc
cp ./warmstart/gdas.20221209/00/RESTART/20221209.000000.fv_core.res.tile1.nc ./fv_core.res.tile1.nc
cp ./coldstart/out.atm.tile1.nc ./out.atm.tile1.nc
cp /lfs/h2/emc/global/noscrub/emc.global/FIX/fix/orog/20220805/C768/C768_grid.tile1.nc .
cp /lfs/h2/emc/global/noscrub/emc.global/FIX/fix/orog/20220805/C768/C768_oro_data.tile1.nc .

python da_chgres_winds.py fv_core.res.tile1.nc out.atm.tile1.nc fv_core.res.nc C768_grid.tile1.nc
#gdb python da_chgres_winds.py
#python -m pdb da_chgres_winds.py # debugger


module load nco
module load gsl
#ncrename -O -v t,T ./out.atm.tile1.nc
#ncdiff -O -v u,v,delp ./out.atm.tile1.nc ./fv_core.res.tile1.nc ./tile1.ncdiff.nc
exit
#python compare_results.py
#ncks -O -v udiff,vdiff,tdiff ./out.atm.tile1.nc ./tile.ncdiff.nc
#scp tile1_chgres_winds.nc Donald.E.Lippi@dtn-hera.fairmont.rdhpcs.noaa.gov/fv3-cam/Donald.E.Lippi/blending_fv3/fv3jedi/glb-test/C768_test/plotting/.
