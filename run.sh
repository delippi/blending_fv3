#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test/blending.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/tmp_ICS_test/blending.err
#PBS -l select=2:ncpus=128
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:45:00

START=$(date +%s)
dom="CONUS"
pdy=20220720
cyc=18
ulimit -s unlimited
export OMP_STACKSIZE=2G
export OMP_NUM_THREADS="96"  #largest value tried that doesn't crash with fastest time = 96 (30s)
                             #1
                             #2
                             #4
                             #13
                             #26
                             #52  (57s)
                             #96  (30s)
                             #128 (32s)
export FI_OFI_RXM_SAR_LIMIT=3145728
export FI_MR_CACHE_MAX_COUNT=0
export MPICH_OFI_STARTUP_CONNECT=1

echo "OMP_STACKSIZE="$OMP_STACKSIZE
echo "OMP_NUM_THREADS="$OMP_NUM_THREADS
echo "domain="${dom}

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/tmp_ICS

echo -ne "Copying files..............\r"
# GDAS FILES
cp ./${dom}/gdas/out.atm.tile7.nc ./out.atm.tile7.nc
cp ./${dom}/gdas/gfs_ctrl.nc      ./gfs_ctrl.nc

# RRFS FILES
cp ./${dom}/rrfs/RESTART/${pdy}.${cyc}0000.fv_core.res.tile1.nc   ./fv_core.res.tile1.nc
cp ./${dom}/rrfs/RESTART/${pdy}.${cyc}0000.fv_tracer.res.tile1.nc ./fv_tracer.res.tile1.nc
cp ./${dom}/rrfs/RESTART/${pdy}.${cyc}0000.fv_core.res.nc         ./fv_core.res.nc

# FIX FILES
FIX_PATH=/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/regional_workflow/fix/lam/
if [[ ${dom} == "CONUS" ]]; then
    FIX_DIR=$FIX_PATH/RRFS_CONUS_3km/
    CRES="C3359"
elif [[ ${dom} == "NA" ]]; then
    FIX_DIR=$FIX_PATH/RRFS_NA_3km/
    CRES="C3463"
fi
cp $FIX_DIR/${CRES}_grid.tile7.nc     ./${CRES}_grid.tile7.nc
cp $FIX_DIR/${CRES}_oro_data.tile7.halo0.nc ./${CRES}_oro_data.tile7.halo0.nc
echo "Copying files.............. Done."

warm=./fv_core.res.tile1.nc
cold=./out.atm.tile7.nc
grid=./${CRES}_grid.tile7.nc
akbk=./fv_core.res.nc
akbkcold=./gfs_ctrl.nc
orog=./C3359_oro_data.tile7.halo0.nc

python da_chgres_winds.py $warm $cold $grid $akbk $akbkcold $orog


# NOW RUN BLENDING STEP
glb=./out.atm.tile7.nc        #This is the glb after wind rotation and vert remapping.
reg=./fv_core.res.tile1.nc    #The warm rrfs restart
trcr=./fv_tracer.res.tile1.nc #RRFS tracer file for sphum

python da_blending_fv3.py $glb $reg $trcr
END=$(date +%s)
DIFF=$((END - START))
echo "Time taken to run the code: $DIFF seconds"
