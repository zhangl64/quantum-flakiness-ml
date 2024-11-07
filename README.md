# detect flaky test in quantum software using classical machine learning approaches

## Abstract 
 This repository is a compaionon page for submission "detect flaky test in quantum software using classical machine learning approaches".

It contains all the material required to reproduce the experiements include: dataset, algorithms, and implementation




## Reproducing results
1. Our experiences are using *python 3.12.2*. You can get the appropriate version for your OS [here](https://www.python.org/downloads/).
2. Based on python, our experience was conducted through *jupyter notebook*. You can get the notebook using PIP command (pip install notebook)
3. In inpyb file, first cells in each model is to preprocessing. First cell must run first before any other cell

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
    |---- Regular model     |    \Machine Learning model that does not use SMOTE and Threshold, includes balance and imbalanced dataset
    |                       |---- Dataset   \Dataset that is extracted from DatasetList, after filtering out setup or util files
    |                       |---- RegularModel_PCA   \scripts to run experience include preprocessing and KNN, SVM and XGB
    |                       |---- RegularModel_nonPCA   \ scripts to run experience include preprocessing and RF and DT
    |                       |---- results   \result of machine learning models in .csv file  
    |
    |---- SMOTE model       |    \ Machine learning model include SMOTE approach
    |                       |---- Dataset   \Dataset that is extracted from DatasetList, after filtering out setup or util files
    |                       |---- SMOTE    \scripts with SMOTE implementation and scripts to run experience include preprocessing
    |                       |---- results   \result of machine learning models in .csv file  
    |
    |---- Thershold         |    \ Machine learing model include Threshold adjustment
    |                       |---- Dataset   \Dataset that is extracted from DatasetList, after filtering out setup or util files
    |                       |---- Thershold_PCA  \scripts to run experience include preprocessing and KNN, SVM and XGB
    |                       |---- Threshold_nonPCA   \ scripts to run experience include preprocessing and RF and DT
    |                       |---- results   \result of machine learning models in .csv file 
    |
    |---- SMOTE+Threshold   |    \Machine learning model include Threshold and SMOTE approach simultainiously
    |                       |---- Dataset   \Dataset that is extracted from DatasetList, after filtering out setup or util files
    |                       |---- PCA_Models   \scripts to run experience include preprocessing and KNN, SVM and XGB
    |                       |---- non_PCA_Models    \ scripts to run experience include preprocessing and RF and DT
    |                       |---- results   \result of machine learning models in .csv file 