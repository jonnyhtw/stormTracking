#!/bin/bash -l

# DIRECTIVES:
#SBATCH --time=24:00:00
##SBATCH --error=storm_detection.err
##SBATCH --out=storm_detection.out
#SBATCH --job-name=storm_detection
#SBATCH --partition=nesi_prepost
#SBATCH --cpus-per-task=1
#SBATCH --account=niwa00013
#SBATCH --hint=nomultithread
##SBATCH --mem-per-cpu=200G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --array=2023

export PATH=/nesi/nobackup/niwa00013/williamsjh/miniconda3/bin:$PATH

source activate master

export dataset='era5'

mkdir -p /nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/$dataset

/nesi/nobackup/niwa00013/williamsjh/miniconda3/envs/master/bin/python -u storm_detection.py --startyear=$SLURM_ARRAY_TASK_ID --dataset=$dataset --model_data=False
