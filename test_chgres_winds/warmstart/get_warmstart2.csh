set datep1=$1
set date=`incdate $datep1 -6`
set datep2=`incdate $date 12`
echo "$date $datep1 $datep2"
set YYYY=`echo $date | cut -c1-4`
set YYYYMM=`echo $date | cut -c1-6`
set YYYYMMDD=`echo $date | cut -c1-8`
set HH=`echo $date | cut -c9-10`
set YYYYp1=`echo $datep1 | cut -c1-4`
set YYYYMMp1=`echo $datep1 | cut -c1-6`
set YYYYMMDDp1=`echo $datep1 | cut -c1-8`
set HHp1=`echo $datep1 | cut -c9-10`
set YYYYp2=`echo $datep2 | cut -c1-4`
set YYYYMMp2=`echo $datep2 | cut -c1-6`
set YYYYMMDDp2=`echo $datep2 | cut -c1-8`
set HHp2=`echo $datep2 | cut -c9-10`
## get control
#set hpssfile=/NCEPPROD/hpssprod/runhistory/rh${YYYY}/${YYYYMM}/${YYYYMMDD}/com_gfs_v16.3_gdas.${YYYYMMDD}_${HH}.gdas_restart.tar
#htar -xvf $hpssfile

#set hpssfile=/NCEPPROD/hpssprod/runhistory/rh${YYYYp1}/${YYYYMMp1}/${YYYYMMDDp1}/com_gfs_v16.3_gdas.${YYYYMMDDp1}_${HHp1}.gdas_restart.tar
#htar -xvf $hpssfile 

/bin/mv -f gdas.${YYYYMMDD}/${HH}/RESTART/${YYYYMMDDp1}.${HHp1}*nc gdas.${YYYYMMDDp1}/${HHp1}/RESTART
exit
/bin/rm -rf gdas.${YYYYMMDD}/${HH}
/bin/rm -f gdas.${YYYYMMDDp1}/${HHp1}/*bufr* gdas.${YYYYMMDDp1}/${HHp1}/*stat*
/bin/rm -f gdas.${YYYYMMDDp1}/${HHp1}/RESTART/${YYYYMMDDp2}.${HHp2}*
/bin/rm -f gdas.${YYYYMMDDp1}/${HHp1}/RESTART/${YYYYMMDD}.${HH}*
ls -l gdas.${YYYYMMDDp1}/${HHp1}
ls -l gdas.${YYYYMMDDp1}/${HHp1}/RESTART
exit

