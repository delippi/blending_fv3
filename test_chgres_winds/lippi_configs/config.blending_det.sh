MACHINE="wcoss2"
version="v0.4.0"
ACCOUNT="RRFS_DEV"
#RESERVATION="rrfsdet"
#EXPT_BASEDIR="YourOwnSpace/${version}"
EXPT_BASEDIR="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/$version/"
EXPT_SUBDIR="RRFS_CONUS_3km"

PREDEF_GRID_NAME=RRFS_CONUS_3km

. set_rrfs_config_general.sh
. set_rrfs_config_SDL_VDL_MixEn.sh

#ACCOUNT="rtwrfruc"
#SERVICE_ACCOUNT="rtwrfruc"
#HPSS_ACCOUNT="nrtrr"
#RESERVATION="rrfsens"
#RESERVATION_POST="rrfsens"
ACCOUNT=RRFS-DEV
HPSS_ACCOUNT="RRFS-DEV"
QUEUE_DEFAULT="dev"
QUEUE_ANALYSIS="dev"
QUEUE_FCST="dev"
QUEUE_HPSS="dev_transfer"
QUEUE_PRDGEN="dev"
QUEUE_GRAPHICS="dev"

CLEAN_OLDPROD_HRS="240"
CLEAN_OLDLOG_HRS="240"
CLEAN_OLDRUN_HRS="24"
CLEAN_OLDFCST_HRS="24"
CLEAN_OLDSTMPPOST_HRS="24"
CLEAN_NWGES_HRS="240"

#DO_ENSEMBLE="TRUE"
#DO_BLENDING="TRUE"
#DO_ENSFCST="TRUE"
DO_DACYCLE="TRUE"
DO_SURFACE_CYCLE="TRUE"
DO_SPINUP="TRUE"
DO_SAVE_INPUT="TRUE"
DO_POST_SPINUP="FALSE"
DO_POST_PROD="TRUE"
DO_RETRO="TRUE"
DO_NONVAR_CLDANAL="TRUE"
DO_ENVAR_RADAR_REF="TRUE"
DO_SMOKE_DUST="FALSE"
DO_REFL2TTEN="FALSE"
RADARREFL_TIMELEVEL=(0)
FH_DFI_RADAR="0.0,0.25,0.5"
DO_SOIL_ADJUST="TRUE"
DO_RADDA="TRUE"
DO_BUFRSND="FALSE"
USE_FVCOM="FALSE"
PREP_FVCOM="FALSE"
DO_PARALLEL_PRDGEN="FALSE"

EXTRN_MDL_ICS_OFFSET_HRS="3"
LBC_SPEC_INTVL_HRS="1"
EXTRN_MDL_LBCS_OFFSET_HRS="0"
BOUNDARY_LEN_HRS="18"
BOUNDARY_PROC_GROUP_NUM="3"

# avaialble retro period:
# 20210511-20210531; 20210718-20210801
DATE_FIRST_CYCL="20220720"
DATE_LAST_CYCL="20220720"
CYCL_HRS=( "00" "12" )
CYCL_HRS_SPINSTART=("03" "15")
CYCL_HRS_PRODSTART=("09" "21")
CYCLEMONTH="07"
CYCLEDAY="20"

STARTYEAR=${DATE_FIRST_CYCL:0:4}
STARTMONTH=${DATE_FIRST_CYCL:4:2}
STARTDAY=${DATE_FIRST_CYCL:6:2}
STARTHOUR="00"
ENDYEAR=${DATE_LAST_CYCL:0:4}
ENDMONTH=${DATE_LAST_CYCL:4:2}
ENDDAY=${DATE_LAST_CYCL:6:2}
ENDHOUR="23"
FIRST_BLENDED_CYCLE="18"  # usually second partial cycle
FIRST_BLENDED_CYCLE_DATE=${STARTYEAR}${STARTMONTH}${STARTDAY}${FIRST_BLENDED_CYCLE}

PREEXISTING_DIR_METHOD="upgrade"
INITIAL_CYCLEDEF="${DATE_FIRST_CYCL}0300 ${DATE_LAST_CYCL}2300 12:00:00"
BOUNDARY_CYCLEDEF="${DATE_FIRST_CYCL}0000 ${DATE_LAST_CYCL}2300 06:00:00"
PROD_CYCLEDEF="00 01,02,04,05,07,08,10,11,13,14,16,17,19,20,22,23 ${CYCLEDAY} ${CYCLEMONTH} ${STARTYEAR} *"
PRODLONG_CYCLEDEF="00 0-23/3 ${CYCLEDAY} ${CYCLEMONTH} ${STARTYEAR} *"
#ARCHIVE_CYCLEDEF="${DATE_FIRST_CYCL}0700 ${DATE_LAST_CYCL}2300 24:00:00"
if [[ $DO_SPINUP == "TRUE" ]] ; then
  SPINUP_CYCLEDEF="00 03-08,15-20 ${CYCLEDAY} ${CYCLEMONTH} ${STARTYEAR} *"
fi

FCST_LEN_HRS="3"
FCST_LEN_HRS_SPINUP="1"
#FCST_LEN_HRS_CYCLES=(48 18 18 18 18 18 48 18 18 18 18 18 48 18 18 18 18 18 48 18 18 18 18 18)
for i in {0..23}; do FCST_LEN_HRS_CYCLES[$i]=3; done
for i in {0..23..3}; do FCST_LEN_HRS_CYCLES[$i]=12; done
DA_CYCLE_INTERV="1"
RESTART_INTERVAL="1"
RESTART_INTERVAL_LONG="1"
## set up post
POSTPROC_LEN_HRS="3"
POSTPROC_LONG_LEN_HRS="12"
NFHOUT_HF="1"
# 15 min output upto 18 hours
#NFHMAX_HF="2"
#NFHOUT="1"
#NSOUT_MIN="15"
#OUTPUT_FH="0.0 0.25 0.50 0.75 1.0 1.25 1.50 1.75 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 12.0"

USE_RRFSE_ENS="TRUE"
CYCL_HRS_HYB_FV3LAM_ENS=("00" "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23")

SST_update_hour=01
GVF_update_hour=04
SNOWICE_update_hour=00
SOIL_SURGERY_time=2022072004
netcdf_diag=.true.
binary_diag=.false.

regional_ensemble_option=5   # 5 for RRFS ensemble

EXTRN_MDL_NAME_ICS="FV3GFS"
EXTRN_MDL_NAME_LBCS="FV3GFS"
FV3GFS_FILE_FMT_ICS="grib2"
FV3GFS_FILE_FMT_LBCS="grib2"

envir="para"

NET="rrfs_b"
TAG="c3v40"

#ARCHIVEDIR="/1year/BMC/wrfruc/rrfs_b"
ARCHIVEDIR="/NCEPDEV/emc-meso/5year/Donald.E.Lippi/blending/retro/rrfs"
NCL_REGION="conus"
MODEL="rrfs_b"
RUN="rrfs"
RUN_ensctrl="rrfs"

. set_rrfs_config.sh

#STMP="YourOwnSpace/${version}/stmp"  # Path to directory STMP that mostly contains input files.
#PTMP="YourOwnSpace/${version}"  # Path to directory STMP that mostly contains input files.
#NWGES="YourOwnSpace/${version}/nwges"  # Path to directory NWGES that save boundary, cold initial, restart files
#STMP="${EXPT_BASEDIR}/stmp"  # Path to directory STMP that mostly contains input files.
#PTMP="${EXPT_BASEDIR}"  # Path to directory STMP that mostly contains input files.
#NWGES="${EXPT_BASEDIR}/nwges"  # Path to directory NWGES that save boundary, cold initial, restart files
STMP="/lfs/h2/emc/stmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}/"
PTMP="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}/"
NWGES="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}/nwges"
ENSCTRL_STMP="/lfs/h2/emc/stmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}/ctrl"
ENSCTRL_PTMP="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}"
ENSCTRL_NWGES="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}/nwges"
if [[ ${regional_ensemble_option} == "5" ]]; then
#  RRFSE_NWGES="YourOwnSpace/${version}/nwges"  # Path to RRFSE directory NWGES that mostly contains ensemble restart files for GSI hybrid.
#  RRFSE_NWGES="${EXPT_BASEDIR}/nwges"  # Path to RRFSE directory NWGES that mostly contains ensemble restart files for GSI hybrid.
  RRFSE_NWGES="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs/July2022_retro/Ens_blending_${BLENDING_LENGTHSCALE}/${version}/nwges"
  NUM_ENS_MEMBERS=30     # FV3LAM ensemble size for GSI hybrid analysis
  CYCL_HRS_PRODSTART_ENS=( "07" "19" )
  DO_ENVAR_RADAR_REF="TRUE"
fi
