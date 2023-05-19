#!/bin/bash
#PBS -N glbchgres
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l place=vscatter,select=2:ncpus=36
#PBS -l walltime=1:20:00
#PBS -j oe



set -x
source /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/env/build_wcoss2_intel.env
module list
export date=2022120900

ulimit -s unlimited
export OMP_STACKSIZE=1G
export OMP_NUM_THREADS="4"
export FI_OFI_RXM_SAR_LIMIT=3145728
export FI_MR_CACHE_MAX_COUNT=0
export MPICH_OFI_STARTUP_CONNECT=1
export NNODES_MAKE_ICS="2"
export PPN_MAKE_ICS="36"
ncores=$(( NNODES_MAKE_ICS*PPN_MAKE_ICS ))
APRUN="mpiexec -n ${ncores} -ppn ${PPN_MAKE_ICS} --cpu-bind core --depth ${OMP_NUM_THREADS}"


YYYY=`echo $date | cut -c1-4`
YYYYMM=`echo $date | cut -c1-6`
YYYYMMDD=`echo $date | cut -c1-8`
HH=`echo $date | cut -c9-10`
MM=`echo $date | cut -c5-6`
DD=`echo $date | cut -c7-8`
WORKDIR=/lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/coldstart/
rm -rf $WORKDIR
mkdir -p $WORKDIR
cd $WORKDIR
sed "s/<YYYYMMDD>/${YYYYMMDD}/g; s/<MM>/${MM}/g; s/<DD>/${DD}/g; s/<HH>/${HH}/g" ${PBS_O_WORKDIR}/config.C768.nml.template > ${WORKDIR}/config.C768.nml
ln -sf ${WORKDIR}/config.C768.nml ./fort.41
ln -sf ${PBS_O_WORKDIR}/chgres_cube .


$APRUN ./chgres_cube




exit
# Threads useful when ingesting spectral gfs sigio files.
# Otherwise set to 1.
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=1024M

export date=2019091918
#export date=2019070412
export date=2022120900

YYYY=`echo $date | cut -c1-4`
YYYYMM=`echo $date | cut -c1-6`
YYYYMMDD=`echo $date | cut -c1-8`
HH=`echo $date | cut -c9-10`
MM=`echo $date | cut -c5-6`
DD=`echo $date | cut -c7-8`
WORKDIR=/scratch2/BMC/gsienkf/whitaker/ics/chgres_cube/${date}/C384/control
rm -fr $WORKDIR
mkdir -p $WORKDIR
cd $WORKDIR

sed "s/<YYYYMMDD>/${YYYYMMDD}/g; s/<MM>/${MM}/g; s/<DD>/${DD}/g; s/<HH>/${HH}/g" ${SLURM_SUBMIT_DIR}/config.C384.hera.nml.template > ${SLURM_SUBMIT_DIR}/config.C384.hera.nml
ln -fs ${SLURM_SUBMIT_DIR}/config.C384.hera.nml ./fort.41

date

srun /scratch2/BMC/gsienkf/whitaker/global-workflow/exec/chgres_cube.exe

date
tiles="tile1 tile2 tile3 tile4 tile5 tile6"
mkdir INPUT
/bin/mv -f gfs_ctrl.nc INPUT
for tile in $tiles; do
  /bin/mv -f out.atm.${tile}.nc INPUT/gfs_data.${tile}.nc
  /bin/mv -f out.sfc.${tile}.nc INPUT/sfc_data.${tile}.nc
done
/bin/cp -f ${SLURM_SUBMIT_DIR}/gdas.${YYYYMMDD}/${HH}/*bias* ../..
ls -l ../../
ls -l ../
ls -l
ls -l INPUT

exit 0

