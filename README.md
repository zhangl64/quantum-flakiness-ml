# Detect flaky tests in quantum software using classical machine learning approaches

## Abstract 
 This repository is a companion page for the submission "Identifying Flaky Tests in Quantum Code: A
Machine Learning Approach.

It contains all the material required to reproduce the experiments including: dataset, algorithms, and implementation




## Reproducing results
1. Our experiences are using *python 3.12.2*. You can get the appropriate version for your OS [here](https://www.python.org/downloads/).
2. clone the repository
  - `git clone  https://github.com/zhangl64/quantum-flakiness-ml'
3. Install the additional Python packages required:
  - `python3 -m pip install -r requirements.txt`
4. In each ipynb file, the first cells in each model are for preprocessing. The first cell must run before any other cell.

## Dataset
Our dataset is in each folder name after the method (in compressed format in the  Dataset folder). Running the first cell of the code will create extracted folder which is to train the model. 


Directory Structure
-----------------------
The directory is structured as follows:

    quantum-flakiness-ml
        |
        |---- DatasetList       |    \Lists of datasets that we used for this project
        |                       |---- code for data retireval\ codes we created to extract flaky and nonflaky datasets from GitHub
        |
        |---- Vanilla+Threshold |    \Models with vanilla and threshold-tuning implementations
        |                       |---- Dataset              \Dataset that is extracted from DatasetList, after filtering out setup or util files
        |                       |---- VanillaModels.ipynb  \Baseline model implementations for both balanced and imbalanced datasets (no balancing techniques applied)
        |                       |---- Threshold.ipynb      \Models with Threshold-tuning
        |                       |---- results              \Results for the Vanilla and Threshold models in .csv file  
        |
        |---- SMOTE+Hybrid      |    \Models with SMOTE and hybrid implementations (both SMOTE & threshold-tuning)
        |                       |---- Dataset       \Dataset that is extracted from DatasetList, after filtering out setup or util files
        |                       |---- SMOTE.ipynb   \Models with SMOTE 
        |                       |---- hybrid.ipynb  \Hydrid models with SMOTE and Threshold-tuning implementations
        |                       |---- results       \Results of SMOTE and hybrid models in .csv file  
