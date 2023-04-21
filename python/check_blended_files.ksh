#!/bin/ksh

module load nco
module load ncview


#var='U,V,T,QVAPOR,PH,P,MU,U10,V10,T2,Q2,PSFC,TH2'
#var='U,PSFC,PH'
var="u,v,T"

# control files
fg1="../fg"

# experiment
fg_blend="../fg_blend.nc"

cd diffs
ncdiff -O -v "$var" $fg1  $fg_blend "fg-fg_blend.nc"
ncview "fg-fg_blend.nc" & 

cd ..
ncview fg_blend.nc &
ncview fg.nc &
ncview bg.nc &





