[![Build Status](https://travis-ci.com/rpc0/2020fa-cookiecutter-csci-ml-rpc0.svg?token=DuzqB2C9jqGBGDcLSRjq&branch=master)](https://travis-ci.com/rpc0/2020fa-cookiecutter-csci-ml-rpc0)

# Cookiecutter for Machine Learning - Regression

## Setup

This [cookiecutter](https://github.com/cookiecutter/cookiecutter) is a fork off ```cookiecutter gh:ionelmc/cookiecutter-pylibrary``` but customized to build regression models and currently compatible with ```sklearn```.  

To generate a project using this cookiecutter, from the parent folder of the folder where you intend to create the ML project, type ```cookiecutter gh:rpc0/2020fa-cookiecutter-csci-ml-rpc0```.

In the cookiecutter menu, choose your options. If you are not part of csci-e-29 organization in github, leave out csci-uils. The files that went into csci-utils are available in the utils folder generated for you; from orchestrate.py file in orchestration folder, remove the 2 occurrences of ```csci-utils``` (leave the ```.``` after ```csci-utils``` in place), and you should be all set.

Sample project built using this cookiecutter-ml is on the [wine dataset](https://github.com/csci-e-29/2020fa-final-project-rpc0).

## Structure of the generated files

Non-alphabetic order - rearranged for explanation
```
project_name  
│
└───orchestration           
│   │   __init__.py
│   │   orchestrate.py      Luigi-based workflow orchestration. Modify train-test split or to add steps
│   
└───preprocess
│   │   __init__.py
│   │   getsource.py        Modify to setup your data source (e.g. folder in s3, local disk, etc)
│   │   cleandata.py        Specify label, and columns to drop. Does most of the rest for you
│   │   extractfeatures.py  Specify feature extraction logic, and columns to drop after extraction
│   │   transform.py        Encodes categorical variables for you. Modify to scale, normalize, etc
│   
└───model
│   │   __init__.py
│   │   trainmodel.py       Specify model
│   │   evaluatemodel.py    Specify evaulation function, e.g. mse
│   
└───visualize
│   │   __init__.py
│   │   visualizefeaturesignificance.py Specify label. It finds most significant features & image
│   │   visualizepredictions.py         It visulizes predictions on test set and error distribution 
│   
└───utils                   Luigi utils currently. Add your own in other folders
    │   __init__.py
│   └───luigi
│       │   ... 
...   
```
plus README.md with this same content, travis.yml to run on travis-ci.com, pytest.ini to specify location of test files, and more


## Dependencies 

Python packages required for the framework which will be automatically installed via Pipfile

```{r}
luigi
s3fs
dask-ml
fastparquet
category-encoders
seaborn
matplotlib
dask[dataframe]
``` 

Packages recommended for use in your code -

```{r}
sklearn
``` 

Other imports used / useful -

```{r}
re
os
numpy
pandas
``` 


## Advanced Python techniques applied 

While this is not an exhaustive list, the following will be useful to brush up on -

- Framework built on cookiecutter for repeatability
- Skeleton of tasks structured with Luigi workflows into microenvironments and guaranteeing idempotency
- Descriptor protocol (in utils) used for composition of classes
- Context managers to define runtime context (```with``` statements in orchestration) 
- Parallel distributed computation, chunked data, lazy loading, etc with dask
- Columnar data storage using Parquet for efficient column-wise operations
- File protocols for .csv, .parquet, .npy, .png using both dask and luigi approaches

Plus proficiency in use of pipenv, travis, github, etc.


## TO DO - Setup:

- Repeated from above: run ```cookiecutter gh:rpc0/2020fa-cookiecutter-csci-ml-rpc0```, and it will create a new folder with the structure above.
- ```cd``` into the folder created from the above step
- Install [pipenv](https://pypi.org/project/pipenv/) ```sudo apt install pipenv``` if you haven't already, and run ```pipenv shell```. This will get you into a pipenv virtual environment.
- Upgrade setuptools because Python virtual environment leaves the old ```pip install --upgrade setuptools```. Without this ```pipenv update``` will fail with AttributeError
- Run ```pipenv install --dev``` and ```pipenv update```. For more, refer to the Run section below.

## TO DO - Modify:

Using the above structure
- Plug in the path to your .csv files into getsource.py
- Specify label on which to train in cleandata.py
- Optionally specify columns to drop in cleandata.py
- Optionally specify feature extraction logic in extractfeatures.py
- Optionally add other transformations in transform.py
- Specify model to use in trainmodel.py
- Optionally add scoring function (such as mse) in evaluate.py
- Specify label for feature significance in visualizefeaturesignificance.py
- Specify label to predict against in visualizepredictions.py
- Specify test cases for the customized or new code

Where indicated as optional, if not already done, simply pass on ddf to the next line of code or return it.

# TO DO - Test and Debug

- To test locally, first install pytest and pytest-cov using ```pipenv install --dev --ignore-pipfile --deploy```, and then run ```pytest --cov-report xml --cov-report term```
- To debug from PyCharm or VSCode start from __main__.py

# TO DO - Run

- Before running, make sure to run ```pipenv update``` and if used and not up to date run ```pipenv install -e git+https://github.com/csci-e-29/2020fa-csci-utils-rpc0#egg=csci_utils```
- To run locally, use ```python -m <project-source-folder-name>```
- To generate luigi graphs, in another terminal window enter the same folder's ```pipenv shell``` and then run luigid. Then modify __main__.py to enable ```luigi.run()```, comment out the luigi ```build```, then run the ```python -m <project-name> --scheduler-host localhost VisualizeFeatureSignificance```, then go to ```http://localhost:8082``` in your browser. Replace ```VisualizeFeatureSignificance``` with other luigi task name as needed.

## Results

Results will be stored in the data/ folder in the overall project folder. 

Non-alphabetic order - rearranged for explanation
```
data  
│
└───CleanData               Dataset after cleanup (dropping columsn, removing nan, etc)
│   │   part.0.parquet
│   │   ...      
│   
└───ExtractFeatures         Dataset after feature engineering / extracted
│   │   part.0.parquet
│   │   ...      
│   
└───TransformData           Dataset after encoding, normalization, scaling, etc
│   │   part.0.parquet
│   │   ...      
│   
└───MakeTrainingSet         Subset of data for training
│   │   part.0.parquet
│   │   ...      
│   
└───MakeTestSet             Subset of data for test
│   │   part.0.parquet
│   │   ...      
│   
└───Model                   Model stored as pckl
│   │   model.pckl
│   │   ...      
│   
└───VisualizeFeatureSignificance    Visualization stored as png
│   │   featuresignificance.png
│   │   ...      
│   
└───EvaluateModel           Predictions stored as .npy
│   │   predictions.npy
│   │   ...      
│   
└───VisualizePredictions    Visualization stored as .png
│   │   predictions.png
│   │   ...      
...   
```

## Future Extensions 

- Hyperparameter tuning
- Support for pandas as first citizen alongside dask
- Support tensorflow and deep learning use-cases
