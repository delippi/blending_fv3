#!/bin/ksh

module load nco
module load ncview


var='U,V,T,QVAPOR,PH,P,MU,U10,V10,T2,Q2,PSFC,TH2'
var='U,PSFC,PH'

# control files
fg_orig="../fg"
fg_blend_ctl="../fg_blend_ctl.nc"
fg_blend_diag_ctl="../fg_blend_diag_ctl.nc"

# experiment
fg_blend="../fg_blend.nc"
fg_blend_diag="../fg_blend_diag.nc"


#rm -f fg_blend_ctl-fg_blend.nc fg_orig-fg_blend_ctl.nc fg_orig-fg_blend.nc
cd diffs


#ncdiff -O -v "$var" $fg_orig  $fg_blend_ctl fg_orig-fg_blend_ctl.nc
#ncdiff -O -v "$var" $fg_orig      $fg_blend fg_orig-fg_blend.nc
#ncdiff -O -v "$var" $fg_blend_ctl      $fg_blend      fg_blend_ctl-fg_blend.nc
#ncdiff -O -v "$var" $fg_blend_diag_ctl $fg_blend      fg_blend_diag_ctl-fg_blend.nc
#ncdiff -O -v "$var" $fg_blend_diag_ctl $fg_blend_ctl  fg_blend_diag_ctl-fg_blend_ctl.nc
#ncdiff -O -v "$var" $fg_blend_diag_ctl $fg_blend_diag fg_blend_diag_ctl-fg_blend_diag.nc

#ncview fg_orig-fg_blend_ctl.nc &
#ncview fg_orig-fg_blend.nc &
#ncview fg_blend_ctl-fg_blend.nc &
#ncview fg_blend_diag_ctl-fg_blend.nc &
#ncview fg_blend_diag_ctl-fg_blend_ctl.nc & 
#ncview fg_blend_diag_ctl-fg_blend_diag.nc &


ncdiff -O -v "$var" $fg_blend_diag $fg_blend fg_blend_diag-fg_blend.nc
ncview fg_blend_diag-fg_blend.nc &



