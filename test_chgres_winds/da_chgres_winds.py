import numpy as np
from netCDF4 import Dataset
import chgres_winds   # might need to rename in the future
import sys
import pdb     # pdb.set_trace() is a helpful debugging tool.
import tictoc  # To use, put /u/donald.e.lippi/bin/python in your PYTHONPATH

tic = tictoc.tic()

#warm = str(sys.argv[1])  # ./fv_core.res.tile1.nc
#cold = str(sys.argv[2])  # ./out.atm.tile1.nc
#grid = str(sys.argv[3])  # ./C768_grid.tile1.nc
#akbk = str(sys.argv[4])  # ./fv_core.res.nc
warm = str("./fv_core.res.tile1.nc")
cold = str("./out.atm.tile1.nc")
grid = str("./C768_grid.tile1.nc")

warmnc = Dataset(warm)
coldnc = Dataset(cold, mode="a")
gridnc = Dataset(grid)


# STEP 1. ROTATE THE WINDS FROM CHGRES
# Data from warm restarts
u = np.float64(warmnc["u"][0, :, :, :])
v = np.float64(warmnc["v"][0, :, :, :])
nlev = np.shape(u)[0] #127,z
nlat = np.shape(u)[1] #769,y
nlon = np.shape(u)[2] #768,x

top=1; bot=128
nlev = coldnc.createDimension("nlev",nlev)  # 127

# Data from cold chgres
u_s = np.float64(coldnc["u_s"][:, :, :])   # (128, 769, 768)
v_s = np.float64(coldnc["v_s"][:, :, :])   # (128, 769, 768)
u_w = np.float64(coldnc["u_w"][:, :, :])   # (128, 768, 769)
v_w = np.float64(coldnc["v_w"][:, :, :])   # (128, 768, 769)

# grid data
gridx = np.float64(gridnc["x"][0:-1:2,0:-1:2]) # get every other value 'til the end.
gridy = np.float64(gridnc["y"][0:-1:2,0:-1:2])

# Fortran wants everything transposed and in fortran array type
gridx = np.asfortranarray(gridx.transpose())
gridy = np.asfortranarray(gridy.transpose())
u_s   = np.asfortranarray(u_s.transpose())
v_s   = np.asfortranarray(v_s.transpose())
u_w   = np.asfortranarray(u_w.transpose())
v_w   = np.asfortranarray(v_w.transpose())

# Initialize some computed fields to zero
ud     = np.float64(0.0*u_s)  # initialize to zero
vd     = np.float64(0.0*u_w)  # initialize to zero

#rotate winds to model d-grid (~30s; nodes=2; cpus=128)
chgres_winds.main(gridx,gridy,u_s,v_s,u_w,v_w,ud,vd)

# tranpose ud, vd back to original shape, cutoff one of levels (there is an extra level),
# add a new variable to the nc file by duplicating the corresponding u/v variable and
# redefining the shape of the array, finally, assign ud/vd into the u/v variable in nc file.
# For ud
ud = np.transpose(ud)
ud = ud[top:bot,:,:]
var_to_duplicate = coldnc.variables["u_s"]
coldnc.createVariable("u", var_to_duplicate.datatype, ('nlev','latp','lon'))
coldnc.variables["u"][:,:,:] = ud
# For vd
vd = np.transpose(vd)
vd = vd[top:bot,:,:]
var_to_duplicate = coldnc.variables["v_w"]
coldnc.createVariable("v", var_to_duplicate.datatype, ('nlev','lat','lonp'))
coldnc.variables["v"][:,:,:] = vd

# for debugging purposes.
if True:
    udiff = u - ud
    var_to_duplicate = coldnc.variables["u_s"]
    coldnc.createVariable("udiff", var_to_duplicate.datatype, ('nlev','latp','lon'))
    coldnc.variables["udiff"][:,:,:] = udiff[:,:,:]
    print(f"udiff min/max={np.min(udiff[:,0:760,0:760])}/{np.max(udiff[:,0:760,0:760])}")
    print(f"udiff mean   ={np.mean(udiff[:,0:760,0:760])}")
    rmse = np.sqrt(np.mean(udiff**2))
    print(f"udiff rmse   ={rmse}")
    print(f"udiff count>1m/s   ={np.sum( np.abs(udiff) > 1 )}")
    max_index = np.argmax(udiff[:,0:760,0:760])
    i,j,k=np.unravel_index(max_index,udiff[:,0:760,0:760].shape)
    print(f"udiff[{i},{j},{k}]={udiff[i,j,k]}")
    print(f"u[{i},{j},{k}]={u[i,j,k]}")
    print(f"ud[{i},{j},{k}]={ud[i,j,k]}")
    us = np.transpose(u_s)
    #us = us[top:bot,:,:]
    vs = np.transpose(v_s)
    #vs = vs[top:bot,:,:]
    print(f"u_s[{i},{j},{k}]={us[i,j,k]}")
    print(f"v_s[{i},{j},{k}]={vs[i,j,k]}")

    vdiff = v - vd
    var_to_duplicate = coldnc.variables["v_w"]
    coldnc.createVariable("vdiff", var_to_duplicate.datatype, ('nlev','lat','lonp'))
    coldnc.variables["vdiff"][:,:,:] = vdiff[:,:,:]

    t_cold = np.transpose(t_cold)
    t_cold = t_cold[top:bot,:,:]
    tdiff = T - t_cold
    var_to_duplicate = coldnc.variables["t"]
    coldnc.createVariable("tdiff", var_to_duplicate.datatype, ('nlev','lat', 'lon'))
    coldnc.variables["tdiff"][:,:,:] = tdiff[:,:,:] 

# close the nc files
warmnc.close()
coldnc.close()
