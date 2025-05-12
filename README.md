# The_DRN_for_HGCAL

To create the pickle files from ROOT trees:  
> cd Picklemaker  
Change the relevant  paths of the input files and the output folder.   
Change the names of branches as needed in the MyExtract_drhits_EtEz.py file and then run :  
> ./MypreparePickles_ES_EE 1 1 1 
This creates the pickle files in chunks of 2M. To combine the chunks, run the command :  
> python3 Combine_pickle.py  

To train the DRN : 
> ./train [Output folder] [folder with pickles] --nosemi --idx_name all --target trueE --in_layers 3 --mp_layers 4 --out_layers 2  --agg_layers 3 --valid_batch_size 50 --train_batch_size 50  --lr_sched Const --max_lr 0.0001 --pool max --ES yes --hidden_dim 64 --n_epochs 100 &>> [Output folder]/training.log  
Replace the variables in [""] with their actual paths.  
The train executable calls Train.py which calls the "DynamicReductionNetwork.py" from models folder.  
Currently the file  DynamicReductionNetworkJit.py is called in DynamicReductionNetwork.py.  
The train command set the hyperparameters of the model.   
The loss function is taken from models/GravNet.py.    
The default loss function (stated in "train")  is "abs_energy_fraction_loss" which is the mean square loss. It gets used by default when the "--nosemi" tag is used.  


