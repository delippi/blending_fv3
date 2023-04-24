#!/bin/bash
#PBS -N blending
#PBS -A RRFS-DEV
#PBS -q dev
##PBS -l nodes=3:ppn=20
#PBS -l place=vscatter,select=2:ncpus=32
#PBS -l walltime=0:40:00
#PBS -j oe

source /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/env/build_wcoss2_intel.env

module list

ulimit -s unlimited
export OMP_STACKSIZE=1G
export OMP_NUM_THREADS="4"
export FI_OFI_RXM_SAR_LIMIT=3145728
export FI_MR_CACHE_MAX_COUNT=0
export MPICH_OFI_STARTUP_CONNECT=1
export NNODES_MAKE_ICS="2"
export PPN_MAKE_ICS="32"
ncores=$(( NNODES_MAKE_ICS*PPN_MAKE_ICS ))
APRUN="mpiexec -n ${ncores} -ppn ${PPN_MAKE_ICS} --cpu-bind core --depth ${OMP_NUM_THREADS}"

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/chgres
$APRUN ./chgres_cube
