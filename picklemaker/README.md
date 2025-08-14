This is the Pickle maker for A to gamma gamma sample pickle files to train the DRN

The inputs given are the x,y,z, E and subdetector flag (for endcaps and preshower) of all rechits within a dR of 0.3 from the supercluster seed.

### DRN Environment 

#### If using the NSM area (Parambrahma), first run the following commands to set up the environment.

```
module load iiser/apps/cuda/11.4 

module load cdac/spack/0.17

source /home/apps/spack/share/spack/setup-env.sh

spack load python@3.8.2

source /home/apps/iiser/pytorch-venv/bin/activate

```
This environment is maintained by IISER Pune.

#### If using a different cluster/GPU where this environment is not available

> Install conda/miniconda

> Copy the .yml file containing the DRN environment details from 

> Create the conda environment using the command  " conda env create -f myenv.yml "


To run the pickle maker 

Change the paths in the nTuple and folder variables in preparePickles_EE_ES as needed.

The exectuable preparePickles_EE_ES calls Extract_drhits_EE_ES.py. If changes needs to be made in the inputs (like rescaling or adding new features) , it should be done in Extract_drhits_EE_ES.py file.

To prepare the pickles, run the following command:

```
 ./preparePickles_EE_ES 1 1 1

```

This prepares pickles in chunks of 2M (to prevent the system from running out of memory).

To combine the chunks of pickle files, assign the path where the chunked pickles are stored to the variable "output_dir"  in Combine_pickle.py . If ES hits are included, change value of "output_file" to "cartfeat_ES.pickle".

Combine the chunked pickles by running the following command:

```
python Combine_pickle.py

```

To train the DRN :

```
[Path to DRN folder]/train [Output folder] [folder with pickles] --nosemi --idx_name all --target trueE --in_layers 3 --mp_layers 4 --out_layers 2  --agg_layers 3 --valid_batch_size 50 --train_batch_size 50  --lr_sched Const --max_lr 0.0001 --pool max --ES yes --hidden_dim 64 --n_epochs 100 &>> [Output folder]/training.log

```

Replace the variables in [""] with their actual paths.

The train executable calls Train.py which calls the "DynamicReductionNetwork.py" from models folder.

Currently the file  DynamicReductionNetworkJit.py is called in DynamicReductionNetwork.py.

The train command sets the hyperparameters of the model.

The loss function is taken from models/GravNet.py.

Use the " --predict_only" tag if you have a pre-trained pytorch model and only want to run inference.


