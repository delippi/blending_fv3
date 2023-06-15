import numpy as np
from netCDF4 import Dataset
import pdb

exp="./out.atm.tile1.compare.nc" # file from chgres_winds; stand-alone program on on wcoss2
ctl1="./fv3-jedi-results/20221209.000000.coldstartwinds.gfs_data.tile1.nc" # fv3-jedi tool
ctl2="./fv3-jedi-results/20221209.000000.cold2fv3.fv_core.res.tile1.nc"    # fv3-jedi tool
ctl3="./fv3-jedi-results/20221209.000000.cold2fv3.fv_tracer.res.tile1.nc"

expnc = Dataset(exp, mode="a")  # write out to this file.
ctl1nc = Dataset(ctl1)
ctl2nc = Dataset(ctl2)
ctl3nc = Dataset(ctl3)

temp=False
ugrd=False

temp_sfc=True
ugrd_sfc=True
delp_sfc=True
sphum_sfc=True

#temp_sfc=False
#ugrd_sfc=False
#delp_sfc=False
#sphum_sfc=False

expnc.createDimension('nlev_1', size=1)
if sphum_sfc:
    print("Working on sphum")
    # Get the variable from each of the 3 files. They all use different names...
    var0 = np.float64(expnc["sphum_cold2fv3"][-1, :, :])# float       t(          lev,     lat,     lon) ;
    var1 = np.float64(ctl1nc["sphum_cold"][0,-1, :, :]) # double t_cold(Time, zaxis_2, yaxis_1, xaxis_1) ;
    var2 = np.float64(ctl3nc["sphum"][0,-1, :, :])      # double      T(Time, zaxis_1, yaxis_2, xaxis_1) ;

    # Compute the diffs.
    diff_chgreswinds_minus_coldstartwinds = var0 - var1
    diff_chgreswinds_minus_cold2fv3 = var0 - var2
    diff_coldstartwinds_minus_cold2fv3 = var1 - var2

    print(var0[693,442])
    print(var1[693,442])
    print(var2[693,442])
    print(np.max(diff_chgreswinds_minus_cold2fv3))

    # Create new variables to store the diffs in.
    var_to_duplicate = expnc.variables["sphum_cold2fv3"]
    expnc.createVariable("sphumdiff_chgreswinds_minus_coldstartwinds", var_to_duplicate.datatype, ('nlev_1','lat','lon'))
    expnc.createVariable("sphumdiff_chgreswinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','lat','lon'))
    expnc.createVariable("sphumdiff_coldstartwinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','lat','lon'))

    # Fill in the new variables with the diff values.
    expnc.variables["sphumdiff_chgreswinds_minus_coldstartwinds"][:,:] = diff_chgreswinds_minus_coldstartwinds[:,:]
    expnc.variables["sphumdiff_chgreswinds_minus_cold2fv3"][:,:] = diff_chgreswinds_minus_cold2fv3[:,:]
    expnc.variables["sphumdiff_coldstartwinds_minus_cold2fv3"][:,:] = diff_coldstartwinds_minus_cold2fv3[:,:]


if delp_sfc:
    print("Working on delp")
    # Get the variable from each of the 3 files. They all use different names...
    var0 = np.float64(expnc["delp_cold2fv3"][-1, :, :])# float       t(          lev,     lat,     lon) ;
    var1 = np.float64(ctl1nc["delp_cold"][0,-1, :, :]) # double t_cold(Time, zaxis_2, yaxis_1, xaxis_1) ;
    var2 = np.float64(ctl2nc["delp"][0,-1, :, :])      # double      T(Time, zaxis_1, yaxis_2, xaxis_1) ;

    # Compute the diffs.
    diff_chgreswinds_minus_coldstartwinds = var0 - var1
    diff_chgreswinds_minus_cold2fv3 = var0 - var2
    diff_coldstartwinds_minus_cold2fv3 = var1 - var2

    print(var0[693,442])
    print(var1[693,442])
    print(var2[693,442])
    print(np.max(diff_chgreswinds_minus_cold2fv3))

    # Create new variables to store the diffs in.
    var_to_duplicate = expnc.variables["delp_cold2fv3"]
    expnc.createVariable("delpdiff_chgreswinds_minus_coldstartwinds", var_to_duplicate.datatype, ('nlev_1','lat','lon'))
    expnc.createVariable("delpdiff_chgreswinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','lat','lon'))
    expnc.createVariable("delpdiff_coldstartwinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','lat','lon'))

    # Fill in the new variables with the diff values.
    expnc.variables["delpdiff_chgreswinds_minus_coldstartwinds"][:,:] = diff_chgreswinds_minus_coldstartwinds[:,:]
    expnc.variables["delpdiff_chgreswinds_minus_cold2fv3"][:,:] = diff_chgreswinds_minus_cold2fv3[:,:]
    expnc.variables["delpdiff_coldstartwinds_minus_cold2fv3"][:,:] = diff_coldstartwinds_minus_cold2fv3[:,:]



if temp_sfc:
    print("Working on temp")
    # Get the variable from each of the 3 files. They all use different names...
    var0 = np.float64(expnc["t_cold2fv3"][-1, :, :])# float       t(          lev,     lat,     lon) ;
    var1 = np.float64(ctl1nc["t_cold"][0,-1, :, :]) # double t_cold(Time, zaxis_2, yaxis_1, xaxis_1) ;
    var2 = np.float64(ctl2nc["T"][0,-1, :, :])      # double      T(Time, zaxis_1, yaxis_2, xaxis_1) ;

    # Compute the diffs.
    diff_chgreswinds_minus_coldstartwinds = var0 - var1
    diff_chgreswinds_minus_cold2fv3 = var0 - var2
    diff_coldstartwinds_minus_cold2fv3 = var1 - var2

    print(var0[693,442])
    print(var1[693,442])
    print(var2[693,442])
    print(np.max(diff_chgreswinds_minus_cold2fv3))

    # Create new variables to store the diffs in.
    var_to_duplicate = expnc.variables["t_cold2fv3"]
    expnc.createVariable("tdiff_chgreswinds_minus_coldstartwinds", var_to_duplicate.datatype, ('nlev_1','lat','lon'))
    expnc.createVariable("tdiff_chgreswinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','lat','lon'))
    expnc.createVariable("tdiff_coldstartwinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','lat','lon'))

    # Fill in the new variables with the diff values.
    expnc.variables["tdiff_chgreswinds_minus_coldstartwinds"][:,:] = diff_chgreswinds_minus_coldstartwinds[:,:]
    expnc.variables["tdiff_chgreswinds_minus_cold2fv3"][:,:] = diff_chgreswinds_minus_cold2fv3[:,:]
    expnc.variables["tdiff_coldstartwinds_minus_cold2fv3"][:,:] = diff_coldstartwinds_minus_cold2fv3[:,:]

if ugrd_sfc:
    print("Working on u sfc")
    # Get the variable from each of the 3 files. They all use different names...
    var0 = np.float64(expnc["u_cold2fv3"][-1, :, :])
    var1 = np.float64(ctl1nc["ud_cold"][0,-1,:,:]) #[0,1:128, :, :])
    var2 = np.float64(ctl2nc["u"][0,-1,:,:]) #[0,:, :, :])

    # Compute the diffs.
    diff_chgreswinds_minus_coldstartwinds = var0 - var1
    diff_chgreswinds_minus_cold2fv3 = var0 - var2
    diff_coldstartwinds_minus_cold2fv3 = var1 - var2

    print(var0[693,442])
    print(var1[693,442])
    print(var2[693,442])
    print(np.max(diff_chgreswinds_minus_cold2fv3[1:760,1:760]))
    print(np.max(diff_coldstartwinds_minus_cold2fv3[1:760,1:760]))

    # Create new variables to store the diffs in.
    var_to_duplicate = expnc.variables["u_cold2fv3"]
    expnc.createVariable("udiff_chgreswinds_minus_coldstartwinds", var_to_duplicate.datatype, ('nlev_1','latp','lon'))
    expnc.createVariable("udiff_chgreswinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','latp','lon'))
    expnc.createVariable("udiff_coldstartwinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev_1','latp','lon'))

    # Fill in the new variables with the diff values.
    expnc.variables["udiff_chgreswinds_minus_coldstartwinds"][:,:] = diff_chgreswinds_minus_coldstartwinds[:,:]
    expnc.variables["udiff_chgreswinds_minus_cold2fv3"][:,:] = diff_chgreswinds_minus_cold2fv3[:,:]
    expnc.variables["udiff_coldstartwinds_minus_cold2fv3"][:,:] = diff_coldstartwinds_minus_cold2fv3[:,:]

if ugrd:
    print("Working on u")
    # Get the variable from each of the 3 files. They all use different names...
    var0 = np.float64(expnc["u"][:, :, :])
    var1 = np.float64(ctl1nc["ud_cold"][0,1:128,:,:]) #[0,1:128, :, :])
    var2 = np.float64(ctl2nc["u"][0,:,:,:]) #[0,:, :, :])

    # Compute the diffs.
    diff_chgreswinds_minus_coldstartwinds = var0 - var1
    diff_chgreswinds_minus_cold2fv3 = var0 - var2
    diff_coldstartwinds_minus_cold2fv3 = var1 - var2

    # Create new variables to store the diffs in.
    var_to_duplicate = expnc.variables["u"]
    expnc.createVariable("udiff_chgreswinds_minus_coldstartwinds", var_to_duplicate.datatype, ('nlev','latp','lon'))
    expnc.createVariable("udiff_chgreswinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev','latp','lon'))
    expnc.createVariable("udiff_coldstartwinds_minus_cold2fv3", var_to_duplicate.datatype, ('nlev','latp','lon'))

    # Fill in the new variables with the diff values.
    expnc.variables["udiff_chgreswinds_minus_coldstartwinds"][:,:,:] = diff_chgreswinds_minus_coldstartwinds[:,:,:]
    expnc.variables["udiff_chgreswinds_minus_cold2fv3"][:,:,:] = diff_chgreswinds_minus_cold2fv3[:,:,:]
    expnc.variables["udiff_coldstartwinds_minus_cold2fv3"][:,:,:] = diff_coldstartwinds_minus_cold2fv3[:,:,:]


expnc.close()
ctl1nc.close()
ctl2nc.close()
