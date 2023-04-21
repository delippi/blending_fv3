#!/bin/bash
##SBATCH --ntasks=60
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=20
#SBATCH -t 0:40:00
#SBATCH -A hfv3gfs
#SBATCH -J blending

module list

ulimit -s unlimited
cd /mnt/lfs1/data_untrusted/Donald.E.Lippi/blending/fv3/chgres
srun ./chgres_cube
