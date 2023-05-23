import numpy as np
from netCDF4 import Dataset
import chgres_winds   # might need to rename in the future
import remap_dwinds
import sys
import pdb     # pdb.set_trace() is a helpful debugging tool.
import tictoc  # To use, put /u/donald.e.lippi/bin/python in your PYTHONPATH

tic = tictoc.tic()

warm = str(sys.argv[1])
cold = str(sys.argv[2])
akbk = str(sys.argv[3])

warm_nc = Dataset(warm)
cold_nc = Dataset(cold, mode="a")
akbk_nc = Dataset(akbk)


# Data from warm restarts
u = np.float64(warm_nc["u"][0, :, :, :])
v = np.float64(warm_nc["v"][0, :, :, :])
#T = np.float64(warm_nc["T"][0, :, :, :])
#delp = np.float64(warm_nc["delp"][0, :, :, :])
#sphum = np.float64(warm_nc["sphum"][0, :, :, :])
nlev = np.shape(u)[0] #127,z
nlat = np.shape(u)[1] #769,y
nlon = np.shape(u)[2] #768,x

top=1; bot=128
nlev = cold_nc.createDimension("nlev",nlev)

# Data from cold chgres
geolon_s = np.float64(cold_nc["geolon_s"][:,:])  # (769, 768)
geolat_s = np.float64(cold_nc["geolat_s"][:,:])  # (769, 768)
geolon_w = np.float64(cold_nc["geolon_w"][:,:])  # (768, 769)
geolat_w = np.float64(cold_nc["geolat_w"][:,:])  # (768, 769)
u_s = np.float64(cold_nc["u_s"][:, :, :])  # (128, 769, 768)
v_s = np.float64(cold_nc["v_s"][:, :, :])  # (128, 769, 768)
u_w = np.float64(cold_nc["u_w"][:, :, :])  # (128, 768, 769)
v_w = np.float64(cold_nc["v_w"][:, :, :])  # (128, 768, 769)
#t_cold    = np.float64(cold_nc["t"][:, :, :])    # (128, 768, 768)
#delp_cold = np.float64(cold_nc["delp"][:, :, :]) # (127, 768, 768)
ps_cold   = np.float64(cold_nc["ps"][:, :])      # (768, 768)

# Data from akbk file
ak = np.float64(akbk_nc["ak"][0, :]) # (128,)
bk = np.float64(akbk_nc["bk"][0, :]) # (128,)

pdb.set_trace()

# Fortran wants everything transposed and in fortran array type
geolon_s = np.asfortranarray(geolon_s.transpose())
geolat_s = np.asfortranarray(geolat_s.transpose())
geolon_w = np.asfortranarray(geolon_w.transpose())
geolat_w = np.asfortranarray(geolat_w.transpose())
u_s    = np.asfortranarray(u_s.transpose())
v_s    = np.asfortranarray(v_s.transpose())
u_w    = np.asfortranarray(u_w.transpose())
v_w    = np.asfortranarray(v_w.transpose())
#t_cold    = np.asfortranarray(t_cold.transpose())
#delp_cold = np.asfortranarray(delp_cold.transpose())
ps_cold   = np.asfortranarray(ps_cold.transpose())

# Initialize some computed fields to zero
ud     = 0*u_s  # initialize to zero
vd     = 0*u_w  # initialize to zero
uf     = 0*u_s  # initialize to zero



#remap non-wind variables
#call remap_scalar(      Atm, levp, npz, ntracers, ak,  bk,   ps,  q, zh,    w,    t)
#subroutine remap_scalar(Atm,   km, npz,    ncnst, ak0, bk0, psc, qa, zh, omga, t_in)
#remap_scalar.main(ak, bk, ps)
#var_to_duplicate = cold_nc.variables["delp"]
#cold_nc.createVariable("delp_dgrid", var_to_duplicate.datatype, ('nlev','lat','lon'))
#cold_nc.variables["delp_dgrid"][:,:,:] = delp


#rotate winds to model d-grid (~30s; nodes=2; cpus=128)
chgres_winds.main(geolon_s,geolat_s,geolon_w,geolat_w,u_s,v_s,u_w,v_w,ud,vd)

#remap wind
npz=128
km=127
#remap_dwinds.main(km, npz, ak, bk, ps_cold, ud, vd)
remap_dwinds.main(km, ak, bk, ps_cold, ud, vd, npz, ak, bk, ps, uf)

ud = uf

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
var_to_duplicate = cold_nc.variables["v_w"]
cold_nc.createVariable("vdiff", var_to_duplicate.datatype, ('nlev','lat','lonp'))
cold_nc.variables["vdiff"][:,:,:] = vdiff[:,:,:]

warm_nc.close()
cold_nc.close()
