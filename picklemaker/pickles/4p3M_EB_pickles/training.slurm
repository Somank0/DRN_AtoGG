#!/bin/bash

#SBATCH --job-name="DRN_residual_train"
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2

source /home/seema/miniconda3/etc/profile.d/conda.sh

conda activate ml

folder="/storage/seema/sosaha/DRN_AtoGG_v2/picklemaker/pickles/4p3M_EB_pickles"

echo "Job started"

/storage/seema/sosaha/DRN_AtoGG_v2/train $folder $folder --nosemi --idx_name all --target trueE --in_layers 3 --mp_layers 4 --out_layers 2  --agg_layers 3 --valid_batch_size 350 --train_batch_size 350  --lr_sched Const --max_lr 0.0001 --pool max --ES no --hidden_dim 64 --n_epochs 200 &>> $folder/training.log 

