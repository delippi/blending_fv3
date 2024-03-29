import numpy as np
from netCDF4 import Dataset
import raymond
import sys
import pdb     # pdb.set_trace() is a helpful debugging tool.
import tictoc  # To use, put /u/donald.e.lippi/bin/python in your PYTHONPATH

tic = tictoc.tic()

# As Lx --> infinity, the final blended fields --> GDAS (e.g., try Lx=2000)
# As Lx --> zero, the final blended fields --> RRFS (e.g., try Lx=50)
Lx = 960  # 960 is suggested in the literature.

pi = np.pi
nbdy = 40  # 20 on each side

blend = False  # True = blend GDAS + RRFS EnKF
               # False = use either GDAS or RRFS EnKF
if not blend:
    use_host_EnKF = True   # True=use GDAS EnKF
                           # False=use RRFS EnKF

# List of variables from the regional (fg) and global (bg) to blend respectively.
vars_fg = ["u", "v", "T", "sphum", "delp"]
vars_bg = ["u_cold2fv3", "v_cold2fv3", "t_cold2fv3", "sphum_cold2fv3", "delp_cold2fv3"]

print("Starting blending")

# GDAS EnKF file chgres_cube-ed from gaussian grid to ESG grid.
# There is one more step to make sure the winds are on the same
# grid staggering and have the same orientation as the RRFS winds.
glb_fg = str(sys.argv[1])
glb_fg_nc = Dataset(glb_fg)
glb_nlon = glb_fg_nc.dimensions["lon"].size  # 1820   (lonp=1821)
glb_nlat = glb_fg_nc.dimensions["lat"].size  # 1092   (latp=1093)
glb_nlev = glb_fg_nc.dimensions["lev"].size  # 66     (levp=67)
glb_Dx = 3.0

# RRFS EnKF restart file fv_core.res.tile1 on ESG grid.
reg_fg = str(sys.argv[2])
# Open the blended file for updating the required vars (use a copy of the regional file)
reg_fg_nc = Dataset(reg_fg, mode="a")
nlon = reg_fg_nc.dimensions["xaxis_1"].size  # 1820   (xaxis_2=1821)
nlat = reg_fg_nc.dimensions["yaxis_2"].size  # 1092   (yaxis_1=1093)
nlev = reg_fg_nc.dimensions["zaxis_1"].size  # 65
Dx = 3.0

# RRFS EnKF restart file fv_tracer.res.tile1 on ESG grid.
reg_fg_t = str(sys.argv[3])
# Open the blended file for updating the required vars (use a copy of the regional file)
reg_fg_t_nc = Dataset(reg_fg_t, mode="a")

# Check matching grids
# Note: global_hyblev_fcst_rrfsL65.txt has 0.000 0.0000000 as the 66th row, so
# don't compare glb_nlev and nlev because glb_nlev will be 66 and nlev will be 65.
# As a work around for now, we will just slice the top (or bottom?) 65 levels of
# the global file and blend those with the regional file.
if (glb_nlon != nlon or glb_nlat != nlat or glb_Dx != Dx):
    print(f"glb_nlon:{glb_nlon} vs nlon:{nlon}")
    print(f"glb_nlat:{glb_nlat} vs nlat:{nlat}")
    print(f"glb_Dx:{glb_Dx}     vs Dx:{Dx}")
    print("grids don't match")
    exit()

eps = (np.tan(pi*Dx/Lx))**-6  # 131319732.431162

print(f"Input")
print(f"  RRFS restart (core)           : {reg_fg}")
print(f"  RRFS restart (tracer)         : {reg_fg_t}")
print(f"  GDAS coldstart from chgres    : {glb_fg}")
print(f"  Lx                            : {Lx}")
print(f"  Dx                            : {Dx}")
print(f"  NLON                          : {nlon}")
print(f"  NLAT                          : {nlat}")
print(f"  NLEV                          : {nlev}")
print(f"  eps                           : {eps}")
print(f"Output")
print(f"  Blended background file       : {reg_fg}, {reg_fg_t}")

# Step 1. blend.
for (var_fg, var_bg) in zip(vars_fg, vars_bg):
    i = vars_fg.index(var_fg)

    if var_fg == "sphum":
        reg_nc = reg_fg_t_nc
    else:
        reg_nc = reg_fg_nc
    glb_nc = glb_fg_nc

    dim = len(np.shape(reg_nc[var_fg]))-1
    if dim == 2:  # 2D vars
        glb = np.float64(glb_nc[var_bg][:, :])     # (1093 1820)
        reg = np.float64(reg_nc[var_fg][:, :, :])  # (1, 1093, 1820)
        ntim = np.shape(reg)[0]
        nlat = np.shape(reg)[1]
        nlon = np.shape(reg)[2]
        nlev = 1
        glb = np.reshape(glb, [ntim, nlat, nlon])  # add time dim bc missing from chgres
        var_out = np.zeros(shape=(nlon, nlat, 1), dtype=np.float64)
        field = np.zeros(shape=(nlon*nlat), dtype=np.float64)
        var_work = np.zeros(shape=((nlon+nbdy), (nlat+nbdy), 1), dtype=np.float64)
        field_work = np.zeros(shape=((nlon+nbdy)*(nlat+nbdy)), dtype=np.float64)
    if dim == 3:  # 3D vars
        glb = np.float64(glb_nc[var_bg][:, :, :])
        reg = np.float64(reg_nc[var_fg][:, :, :, :])  # (1, 65, 1093, 1820)
        ntim = np.shape(reg)[0]
        nlev = np.shape(reg)[1]
        nlat = np.shape(reg)[2]
        nlon = np.shape(reg)[3]
        glb = np.reshape(glb, [ntim, nlev, nlat, nlon])  # add time dim bc missing from chgres
        var_out = np.zeros(shape=(nlon, nlat, nlev, 1), dtype=np.float64)
        field = np.zeros(shape=(nlon*nlat, nlev), dtype=np.float64)
        var_work = np.zeros(shape=((nlon+nbdy), (nlat+nbdy), nlev, 1), dtype=np.float64)
        field_work = np.zeros(shape=((nlon+nbdy)*(nlat+nbdy), nlev), dtype=np.float64)
    glbT = np.transpose(glb)        # (1820, 1093, 65)
    regT = np.transpose(reg)        # (1820, 1093, 65, 1)

    nlon_start = int(nbdy/2)
    nlon_end = int(nlon+nbdy/2)
    nlat_start = int(nbdy/2)
    nlat_end = int(nlat+nbdy/2)

    if blend:
        print(f"Blending backgrounds for {var_fg}/{var_bg}")
        var_work[nlon_start:nlon_end, nlat_start:nlat_end, :] = glbT - regT
        field_work = var_work.reshape((nlon+nbdy)*(nlat+nbdy), nlev, order="F")  # order="F" (FORTRAN)
        field_work = raymond.raymond(field_work, nlon+nbdy, nlat+nbdy, eps, nlev)
        var_work = field_work.reshape(nlon+nbdy, nlat+nbdy, nlev, order="F")
        var_out = var_work[nlon_start:nlon_end, nlat_start:nlat_end, :]
        if dim == 2:  # 2D vars
            var_out = var_out[:, :, 0] + regT[:, :, 0]
            var_out = np.reshape(var_out, [nlon, nlat, 1])  # add the time ("1") dimension back
        if dim == 3:  # 3D vars
            var_out = var_out + regT[:, :, :, 0]
            var_out = np.reshape(var_out, [nlon, nlat, nlev, 1])  # add the time ("1") dimension back
    else:  # skip blending and use either host enkf (GDAS) or the RRFS enkf
        print(f"Blending code is NOT executing blending!")
        print(f"    This is used for finishing converting the cold start files into warm start format.")
        if use_host_EnKF:
            print(f"---> Use the GDAS EnKF")
            var_out = glbT
        else:
            print(f"---> Use the RRFS EnKF")
            var_out = regT

    var_out = np.transpose(var_out)  # (1, 50, 834, 954)

    # Overwrite blended fields to blended file.
    if dim == 2:  # 2D vars
        reg_nc.variables[var_fg][:, :, :] = var_out
    if dim == 3:  # 3D vars
        reg_nc.variables[var_fg][:, :, :, :] = var_out

# Close nc files
reg_nc.close()  # blended file
glb_nc.close()

print("Blending finished successfully.")
tictoc.toc(tic, "Done. ")

exit(0)
