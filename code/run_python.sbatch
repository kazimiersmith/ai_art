#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=60GB
#SBATCH --job-name=prepare_data
#SBATCH --output=prepare_data.out

module purge;
source /scratch/kas1112/.virtualenvs/py_ai_art/bin/activate
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK;
python python/prepare_data.py
python python/prepare_post_panel.py
python python/prepare_commenter_panel.py
python python/prepare_author_panel.py
python python/figures.py

