import numpy as np
from netCDF4 import Dataset
import raymond
import remap
import sys
#import pdb
import tictoc

tic = tictoc.tic()
Lx = 960.0
pi = np.pi
nbdy = 40  # 20 on each side
blend = True

# Eventually, these two lists should be the same. There is still some technical work
# to be done to make sure the chgres_cube output (coldstart) matches the same grid
# staggering as the RRFS restart (warm start).
# https://github.com/NOAA-GFDL/GFDL_atmos_cubed_sphere/blob/bdeee64e860c5091da2d169b1f4307ad466eca2c/tools/external_ic.F90#L433
# https://dtcenter.org/sites/default/files/events/2020/20201105-1300p-fv3-gfdl-1.pdf (slides 15-16)
vars_fg = ["u", "v", "T", "sphum", "delp"]
vars_bg = ["u", "v", "t", "sphum", "delp"]
#vars_fg = ["u"]
#vars_bg = ["u"]
# reads in data after it has been preprocessed with chgres_cube and has been
# horizontally interpolated to the current cubed-sphere grid.
# variables read in from 'gfs_data.nc'
#       u_w -  D-grid west  face tangential wind component (m/s)
#       v_w -  D-grid west  face normal wind component (m/s)
#       u_s -  D-grid south face tangential wind component (m/s)
#       v_s -  D-grid south face normal wind component (m/s)


def inner_prod(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]


if blend:
    print("Starting blending")

    # GDAS EnKF file chgres_cube-ed from gaussian grid to ESG grid.
    # There is one more step to make sure the winds are on the same
    # grid staggering and have the same orientation as the RRFS winds.
    glb_fg = str(sys.argv[1])
    glb_fg_nc = Dataset(glb_fg)
    #glb_fg_nc = Dataset(glb_fg, mode="a")
    glb_nlon = glb_fg_nc.dimensions["lon"].size  # 1820   (lonp=1821)
    glb_nlat = glb_fg_nc.dimensions["lat"].size  # 1092   (latp=1093)
    glb_nlev = glb_fg_nc.dimensions["lev"].size  # 65     (levp=66)
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
    # As a work around for now, we will just slice the top 65 levels of the global file
    # and blend those with the regional file. The 66th level (bottom level) will not
    # be changed since that level doesn't exist in the regional file. We may want to run
    # chgres on the regional file to fix the differences in levels and to update more than
    # just u_s and v_w; we might need to also update u_w and v_s.
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

    winds_done = False  # initialize to false.
    # Step 1. blend.
    for (var_fg, var_bg) in zip(vars_fg, vars_bg):
        i = vars_fg.index(var_fg)
        print(f"Blending backgrounds for {var_fg}/{var_bg}")

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
            # Remap winds to the compute domain (from D-grid)
            # see: /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/src/ufs_weather_model/FV3/atmos_cubed_sphere/tools/external_ic.F90

# use fv_grid_utils_mod, only: mid_pt_sphere, get_unit_vect2, get_latlon_vector

            nhalo_model = 3
            if var_bg == "u" or var_bg == "v" and not winds_done:
                #grid = Dataset("./C3359_grid.tile7.halo4.nc")
                bd = Dataset("./gfs.bndy.nc")
                # /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/ufs-srweather-app/src/
                # ./ufs_weather_model/FV3/atmos_cubed_sphere/model/fv_regional_bc.F90

                isg = 0
                ieg = nlon - 1
                jsg = 0
                jeg = nlat - 1
                isd = isg - nhalo_model
                ied = ieg + nhalo_model
                jsd = jsg - nhalo_model
                jed = jeg + nhalo_model
                u_s = np.float64(glb_nc["u_s"][:, :, :])     # (66, 1093, 1820)
                v_s = np.float64(glb_nc["v_s"][:, :, :])     # (66, 1093, 1820)
                u_w = np.float64(glb_nc["u_w"][:, :, :])     # (66, 1092, 1821)
                v_w = np.float64(glb_nc["v_w"][:, :, :])     # (66, 1092, 1821)
                geolon_s = np.float64(glb_nc["geolon_s"][:,:])
                geolat_s = np.float64(glb_nc["geolat_s"][:,:])
                geolon_w = np.float64(glb_nc["geolon_w"][:,:])
                geolat_w = np.float64(glb_nc["geolat_w"][:,:])

                # Fortran wants everything transposed and in fortran array type
                geolon_s = np.asfortranarray(geolon_s.transpose())
                geolat_s = np.asfortranarray(geolat_s.transpose())
                geolon_w = np.asfortranarray(geolon_w.transpose())
                geolat_w = np.asfortranarray(geolat_w.transpose())
                u_s    = np.asfortranarray(u_s.transpose())
                v_s    = np.asfortranarray(v_s.transpose())
                u_w    = np.asfortranarray(u_w.transpose())
                v_w    = np.asfortranarray(v_w.transpose())
                ud     = 0*u_s
                vd     = 0*u_w

                # Do I need to use a boundary? I think I'm getting nans along the boundary.
                remap.main(geolon_s,geolat_s,geolon_w,geolat_w,isg+1,ieg+1,jsg+1,jeg+1,u_s,v_s,u_w,v_w,ud,vd)

                # do I also need the remap_dwinds routine?
                winds_done = True
            elif not var_bg == "u" and not var_bg == "v" :
                glb = np.float64(glb_nc[var_bg][0:65, :, :])     # (65, 1093, 1820)

            if var_bg == "u" and winds_done:
                glb = np.transpose(ud[:, :, 0:65])
            if var_bg == "v" and winds_done:
                glb = np.transpose(vd[:, :, 0:65])

            #print(np.max(glb))
            #print(np.where(np.isnan(glb)))
            #pdb.set_trace()
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
