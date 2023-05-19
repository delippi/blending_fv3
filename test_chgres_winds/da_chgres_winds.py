import numpy as np
from netCDF4 import Dataset
import remap   # might need to rename in the future
import sys
import pdb     # pdb.set_trace() is a helpful debugging tool.
import tictoc  # To use, put /u/donald.e.lippi/bin/python in your PYTHONPATH

tic = tictoc.tic()

warm = str(sys.argv[1])
cold = str(sys.argv[2])

warm_nc = Dataset(warm)
cold_nc = Dataset(cold, mode="a")


# Data from warm restarts
u = np.float64(warm_nc["u"][0, :, :, :])
v = np.float64(warm_nc["v"][0, :, :, :])
nlev = np.shape(u)[0] #127,z
nlat = np.shape(u)[1] #769,y
nlon = np.shape(u)[2] #768,x


# Data from cold chgres
u_s = np.float64(cold_nc["u_s"][:, :, :])
v_s = np.float64(cold_nc["v_s"][:, :, :])
u_w = np.float64(cold_nc["u_w"][:, :, :])
v_w = np.float64(cold_nc["v_w"][:, :, :])
geolon_s = np.float64(cold_nc["geolon_s"][:,:])
geolat_s = np.float64(cold_nc["geolat_s"][:,:])
geolon_w = np.float64(cold_nc["geolon_w"][:,:])
geolat_w = np.float64(cold_nc["geolat_w"][:,:])

# Fortran wants everything transposed and in fortran array type
geolon_s = np.asfortranarray(geolon_s.transpose())
geolat_s = np.asfortranarray(geolat_s.transpose())
geolon_w = np.asfortranarray(geolon_w.transpose())
geolat_w = np.asfortranarray(geolat_w.transpose())
u_s    = np.asfortranarray(u_s.transpose())
v_s    = np.asfortranarray(v_s.transpose())
u_w    = np.asfortranarray(u_w.transpose())
v_w    = np.asfortranarray(v_w.transpose())
ud     = 0*u_s  # initialize to zero
vd     = 0*u_w  # initialize to zero

remap.main(geolon_s,geolat_s,geolon_w,geolat_w,u_s,v_s,u_w,v_w,ud,vd)

nlev = cold_nc.createDimension("nlev",nlev)
top=1
bot=128

ud = np.transpose(ud)
ud = ud[top:bot,:,:]
var_to_duplicate = cold_nc.variables["u_s"]
cold_nc.createVariable("u", var_to_duplicate.datatype, ('nlev','latp','lon'))
cold_nc.variables["u"][:,:,:] = ud

vd = np.transpose(vd)
vd = vd[top:bot,:,:]
var_to_duplicate = cold_nc.variables["v_w"]
cold_nc.createVariable("v", var_to_duplicate.datatype, ('nlev','lat','lonp'))
cold_nc.variables["v"][:,:,:] = vd

udiff = u - ud
var_to_duplicate = cold_nc.variables["u_s"]
cold_nc.createVariable("udiff", var_to_duplicate.datatype, ('nlev','latp','lon'))
cold_nc.variables["udiff"][:,:,:] = udiff[:,:,:]
print(f"udiff min/max={np.min(udiff[:,0:760,0:760])}/{np.max(udiff[:,0:760,0:760])}")

vdiff = v - vd
var_to_duplicate = cold_nc.variables["v_w"]
cold_nc.createVariable("vdiff", var_to_duplicate.datatype, ('nlev','lat','lonp'))
cold_nc.variables["vdiff"][:,:,:] = vdiff[:,:,:]

warm_nc.close()
cold_nc.close()
