# detect flaky test in quantum software using classical machine learning approaches

## Abstract 
 This repository is a compaionon page for submission "detect flaky test in quantum software using classical machine learning approaches".

It contains all the material required to reproduce the experiements include: dataset, algorithms, and implementation




## Reproducing results
1. Our experiences are using *python 3.12.2*. You can get the appropriate version for your OS [here](https://www.python.org/downloads/).
2. clone the repository
  [here](https://github.com/zhangl64/quantum-flakiness-ml).
3. Install the additional python packages required:
 [here](python -m pip install -r requirements.txt).
4. In inpyb file, first cells in each model is to preprocessing. First cell must run first before any other cell

## Dataset
our dataset is in each folder name after method (in compresed format in Dataset folder). Running first cell of the code will create extracted folder which is to train the model. 


Directory Structure
-----------------------
The dirctory is structured as follows:

    quantum-flakiness-ml
        |
        |---- DatasetList       |    \Lists of dataset that we used for this project
        |                       |---- code for data retireval\ codes we created to extract flaky and nonflaky dataset from github
        |
        |---- Regular model     |    \Machine Learning model that does not use SMOTE or any other method to reslove imbalance dataset
        |                       |---- Dataset   \Dataset that is extracted from DatasetList, after filtering out setup or util files
        |                       |---- VanillaModels.inpyb \ Machine Learning model that does not use SMOTE and Threshold, includes balance and imbalanced dataset
        |                       |----Threshold.inpyb \ Machine learing model include Threshold adjustment
        |                       |---- results   \result of machine learning models in .csv file  
        |
        |---- SMOTE             |    \ Machine learning model include SMOTE approach
        |                       |---- Dataset   \Dataset that is extracted from DatasetList, after filtering out setup or util files
        |                       |---- SMOTE.inpyb    \scripts with SMOTE implementation and scripts to run experience include preprocessing
        |                       | \Machine learning model include Threshold and SMOTE approach simultainiously
        |                       |---- results   \result of machine learning models in .csv file  