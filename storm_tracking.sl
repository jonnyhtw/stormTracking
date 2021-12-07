#!/bin/bash -l

# DIRECTIVES:
#SBATCH --time=24:00:00
#SBATCH --job-name=storm_tracking
#SBATCH --partition=nesi_prepost
#SBATCH --cpus-per-task=1
#SBATCH --account=niwa00013
#SBATCH --hint=nomultithread
##SBATCH --mem-per-cpu=200G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=1989-2008

export PATH=/nesi/nobackup/niwa00013/williamsjh/miniconda3/bin:$PATH

source activate master

export dataset='jra'

/nesi/nobackup/niwa00013/williamsjh/miniconda3/envs/master/bin/python  -u storm_tracking.py --startyear=$SLURM_ARRAY_TASK_ID --dataset=$dataset
