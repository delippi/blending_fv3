import tictoc
tic = tictoc.tic()
import numpy as np
import os as _os
import emcpy.utils.dateutils as _dateutils
from netCDF4 import Dataset
import raymond
import balance
import shutil
import pdb

model = "WRF"
host = "WRF"
Lx = 960.0
pi = np.pi
variables = ["U", "V", "T", "QVAPOR", "PH", "P", "MU", "U10", "V10", "T2", "Q2", "PSFC", "TH2"]
nbdy = 40  # 20 on each side
blend = True
diagnose = True

if blend:
    print("Starting blending")
    #"/mnt/lfs4/BMC/wrfruc/RAPv5_may2021/cycle/boundary/wrfinput_d01_2021-05-13_00_00_00"
    glb_fg = "./bg"
    glb_fg_nc = Dataset(glb_fg)
    glb_nlon = glb_fg_nc.dimensions["west_east_stag"].size
    glb_nlon = glb_fg_nc.dimensions["west_east"].size
    glb_nlat = glb_fg_nc.dimensions["south_north"].size
    glb_nlev = glb_fg_nc.dimensions["bottom_top"].size
    glb_Dx = glb_fg_nc.DX / 1000.0  # convert to km (13.5450869140625)

    #"/mnt/lfs4/BMC/wrfruc/RAPv5_may2021/cycle_test1/2021051223/wrfprd/wrfout_d01_2021-05-13_00_00_00"
    print("copying file...")
    shutil.copyfile("./fg","./fg_blend.nc")
    print("copy done.")
    reg_fg = "./fg_blend.nc"
    # Open the blended file for updating the required vars (use a copy of the regional file)
    reg_fg_nc = Dataset(reg_fg, mode="a")
    nlon = reg_fg_nc.dimensions["west_east_stag"].size
    nlon = reg_fg_nc.dimensions["west_east"].size
    nlat = reg_fg_nc.dimensions["south_north"].size
    nlev = reg_fg_nc.dimensions["bottom_top"].size
    Dx = reg_fg_nc.DX / 1000.0  # convert to km (13.5450869140625)

    # Check matching grids
    if (glb_nlon != nlon or glb_nlat != nlat or glb_nlev != nlev or glb_Dx != Dx):
        print("grids don't match")
        exit()

    eps = (np.tan(pi*Dx/Lx))**-6  # 131319732.431162

    print(f"Input")
    print(f"  regional forecast             : reg_fg ({model})")
    print(f"  host model analysis/forecast  : glb_fg ({host})")
    print(f"  Lx                            : {Lx}")
    print(f"  Dx                            : {Dx}")
    print(f"  NLON                          : {nlon}")
    print(f"  NLAT                          : {nlat}")
    print(f"  NLEV                          : {nlev}")
    print(f"  eps                           : {eps}")
    print(f"Output")
    print(f"  Blended background file       : {reg_fg}")

    # print(raymond.raymond.__doc__)
    # print(raymond.impfila.__doc__)
    # print(raymond.filsub.__doc__)
    # print(raymond.invlow_v.__doc__)
    # print(raymond.rhsini.__doc__)

    # Step 1. blend.
    for var in variables:
        i = variables.index(var)
        print(f"Blending backgrounds for {var}")

        dim = len(np.shape(glb_fg_nc[var]))-1
        if dim == 2:  #2D vars
           glb = np.float64(glb_fg_nc[var][:,:,:])  # (1, 834, 954)
           reg = np.float64(reg_fg_nc[var][:,:,:])  # (1, 834, 954)
           ntim = np.shape(reg)[0]
           nlat = np.shape(reg)[1]
           nlon = np.shape(reg)[2]
           nlev = 1
           var_out = np.zeros(shape=(nlon, nlat, 1), dtype=np.float64)
           field = np.zeros(shape=(nlon*nlat), dtype=np.float64)
           var_work = np.zeros(shape=((nlon+nbdy), (nlat+nbdy), 1), dtype=np.float64)
           field_work = np.zeros(shape=((nlon+nbdy)*(nlat+nbdy)), dtype=np.float64)
        if dim == 3:  #3D vars
           glb = np.float64(glb_fg_nc[var][:,:,:,:])  # (1, 50, 834, 954)
           reg = np.float64(reg_fg_nc[var][:,:,:,:])  # (1, 50, 834, 954)
           ntim = np.shape(reg)[0]
           nlev = np.shape(reg)[1]
           nlat = np.shape(reg)[2]
           nlon = np.shape(reg)[3]
           var_out = np.zeros(shape=(nlon, nlat, nlev, 1), dtype=np.float64)
           field = np.zeros(shape=(nlon*nlat, nlev), dtype=np.float64)
           var_work = np.zeros(shape=((nlon+nbdy), (nlat+nbdy),nlev, 1), dtype=np.float64)
           field_work = np.zeros(shape=((nlon+nbdy)*(nlat+nbdy),nlev), dtype=np.float64)
        glbT= np.transpose(glb)        # (954, 834, 50, 1)
        regT= np.transpose(reg)        # (954, 834, 50, 1)


        nlon_start=int(nbdy/2)-1  # python indicies start at 0; subtract 1
        nlon_end = int(nlon+nbdy/2)-1
        nlat_start=int(nbdy/2)-1
        nlat_end = int(nlat+nbdy/2)-1

        var_work[nlon_start:nlon_end, nlat_start:nlat_end, :] = glbT - regT
        field_work = var_work.reshape((nlon+nbdy)*(nlat+nbdy), nlev, order="F") #order="F" (FORTRAN)
        field_work = raymond.raymond(field_work, nlon+nbdy, nlat+nbdy, eps, nlev)
        var_work = field_work.reshape(nlon+nbdy, nlat+nbdy, nlev, order="F")
        var_out = var_work[nlon_start:nlon_end, nlat_start:nlat_end, :]
        if dim == 2:  #2D vars
            var_out = var_out[:,:,0] + regT[:,:,0]
            var_out = np.reshape(var_out,[nlon, nlat, 1])  # add the time ("1") dimension back
        if dim == 3:  #3D vars
            var_out = var_out + regT[:,:,:,0]
            var_out = np.reshape(var_out,[nlon, nlat, nlev, 1])  # add the time ("1") dimension back
        var_out = np.transpose(var_out)  # (1, 50, 834, 954)

        # Overwrite blended fields to blended file.
        if dim == 2:  #2D vars
            reg_fg_nc.variables[var][:,:,:] = var_out
        if dim == 3:  #3D vars
            reg_fg_nc.variables[var][:,:,:,:] = var_out

    # Close nc files
    reg_fg_nc.close()  # blended file
    glb_fg_nc.close()

    print("Step 1 blending finished successfully.")

if diagnose:
    print("Starting diagnose")
 # Step 2. diagnose.
    print("copying file...")
    shutil.copyfile("./fg_blend.nc","./fg_blend_diag.nc")
    print("copy done.")
    reg_fg = "./fg"
    reg_fgb = "./fg_blend.nc"
    reg_fgd = "./fg_blend_diag.nc"

    print(f"Input")
    print(f"  regional forecast             : {reg_fg}  ({model})")
    print(f"  blended background            : {reg_fgb} ({model})")
    print(f"Output")
    print(f"  diagnosed background file     : {reg_fgd}")

    reg_fg_nc = Dataset(reg_fg)
    reg_fgb_nc = Dataset(reg_fgb)
    reg_fgd_nc = Dataset(reg_fgd, mode="a")  # open with overwrite var permission

    #  vNam(1)="P_TOP"
    #  vNam(2)="RDN"
    #  vNam(3)="RDNW"
    #  vNam(4)="ZNU"
    #  vNam(5)="DNW"
    #  vNam(6)="HGT"
    #  vNam(7)="PSFC"
    #  vNam(8)="MUB"
    #  vNam(9)="MU"
    #  vNam(10)="PHB"
    #  vNam(11)="PH"
    #  vNam(12)="QVAPOR"
    #  vNam(13)="T"

    fg_01 = np.transpose(reg_fg_nc["P_TOP"][0])           # Time
    fg_02 = np.transpose(reg_fg_nc["RDN"][0,:])           # Time, bottom_top
    fg_03 = np.transpose(reg_fg_nc["RDNW"][0,:])          # "
    fg_04 = np.transpose(reg_fg_nc["ZNU"][0,:])           # "
    fg_05 = np.transpose(reg_fg_nc["DNW"][0,:])           # "
    fg_06 = np.transpose(reg_fg_nc["HGT"][0,:])           # "
    fg_07 = np.transpose(reg_fg_nc["PSFC"][0,:,:])        # Time, south_north, west_east
    fg_08 = np.transpose(reg_fg_nc["MUB"][0,:,:])         # "
    fg_09 = np.transpose(reg_fg_nc["MU"][0,:,:])          # "
    fg_10 = np.transpose(reg_fg_nc["PHB"][0,:,:,:])  # Time, bottom_top_stag, south_north, west_east
    fg_11 = np.transpose(reg_fg_nc["PH"][0,:,:,:])        # "
    fg_12 = np.transpose(reg_fg_nc["QVAPOR"][0,:,:,:])    # Time, bottom_top, south_north, west_east
    fg_13 = np.transpose(reg_fg_nc["T"][0,:,:,:])         # "

    fgb_07 = np.transpose(reg_fgb_nc["PSFC"][0,:,:])      # Time, south_north, west_east 
    fgb_12 = np.transpose(reg_fgb_nc["QVAPOR"][0,:,:,:])  # Time, bottom_top, south_north, west_east
    fgb_13 = np.transpose(reg_fgb_nc["T"][0,:,:,:])       # "

    diff_12 = fgb_12 - fg_12  # QVAPOR
    diff_13 = fgb_13 - fg_13  # T
    diff_07 = fgb_07 - fg_07  # PSFC

    # use fg_11 here for shape of PH and MU.
    nlon = np.shape(fg_11)[0]
    nlat = np.shape(fg_11)[1]
    nlev = np.shape(fg_11)[2]
    ii = nlon
    jj = nlat
    kk = nlev

    PH = np.zeros(shape=(ii, jj, kk), dtype=np.float64)
    MU_2d = np.zeros(shape=(ii, jj), dtype=np.float64)

    # Convert arrays to fortran arrays before passing to f2py module (otherwise we will get an error).
    PH = np.asfortranarray(PH)
    MU_2d = np.asfortranarray(MU_2d)

    # Call balance
    (PH, MU_2d) = balance.balance(diff_12, fg_12, fg_11, fg_10, fg_13, diff_13, fg_09, diff_07, fg_08, fg_06, fg_05, fg_04, fg_03, fg_02, fg_01, PH, MU_2d, ii, jj, kk)

    PH = np.reshape(PH,[nlon, nlat, nlev, 1])  # add the time dimension back in
    MU_2d = np.reshape(MU_2d,[nlon, nlat, 1])  # add the time dimension back in

    reg_fgd_nc.variables["PH"][:,:,:,:] = np.transpose(PH)
    reg_fgd_nc.variables["MU"][:,:,:] = np.transpose(MU_2d)

    # Close nc files
    reg_fg_nc.close()   # regional background
    reg_fgb_nc.close()  # blended file
    reg_fgd_nc.close()  # diagnosed file, PH and MU overwritten


    print("Step 2 diagnose finished successfully.")
tictoc.toc(tic, "Done. ")
exit(0)
