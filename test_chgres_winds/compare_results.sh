#!/bin/bash -l
#PBS -j oe
#PBS -o /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/step1.out
#PBS -e /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds/step1.err
##PBS -l select=2:ncpus=128
#PBS -l select=1:ncpus=1
#PBS -A RRFS-DEV
#PBS -q dev
#PBS -l walltime=000:45:00

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/blending/blending_fv3/test_chgres_winds
module load gsl nco

cp out.atm.tile1.nc out.atm.tile1.compare.nc

python compare_results.py

vars="udiff_chgreswinds_minus_coldstartwinds,udiff_chgreswinds_minus_cold2fv3,udiff_coldstartwinds_minus_cold2fv3"
vars="$vars,tdiff_chgreswinds_minus_coldstartwinds,tdiff_chgreswinds_minus_cold2fv3,tdiff_coldstartwinds_minus_cold2fv3"
vars="$vars,delpdiff_chgreswinds_minus_coldstartwinds,delpdiff_chgreswinds_minus_cold2fv3,delpdiff_coldstartwinds_minus_cold2fv3"
vars="$vars,sphumdiff_chgreswinds_minus_coldstartwinds,sphumdiff_chgreswinds_minus_cold2fv3,sphumdiff_coldstartwinds_minus_cold2fv3"


ncks -O -v $vars out.atm.tile1.compare.nc out.atm.tile1.compare.nc
