# Notes
Minimal personal notes along the way.

# TOC

* [Experiment Tracking](#experiment-tracking): definition and goals; MLflow;

# Experiment Tracking

Experiment tracking is the process of keeping track of all **relevant information** (depends on the ML experiment; such as, Source Code, Environment, Data, Model, Hyperparameters, Metrics, ...) from an **ML Experiment** (:is the whole process of ML engineering which could consist of several Experiment *runs*, has *artifacts* i.e. any file associated with the run, and experiment *metadata*).

Goal is: **reproducability**, **organization**, **optimization**

**MLflow** is a open source python package installable with pip or conda, and contains four main modules:
* Tracking: Organizes ML experiment into several runs and keeps track of: Parameters, Metrics, metadata, artifacts (e.g. visualization), and models. MLflow also tracks additional information: source code, git version of the code, start and end time, author. 
* Models
* Model Registry
* Projects

### MLflow backend
To launch MLflow UI with a backend (possible options are sqlite, postgres, mssql, etc.) use: ```mlflow ui --backend-store-uri sqlite:///mlflow.db```

## How to use
* ```mlflow.set_backend_uri("sqlite:///mlflow.db")```
* ```mlflow.set_experiment("name")``` to set an experiment to add runs if already exists or to create new one.
* ```with mlflow.start_run():```: enclosed with the lines of code to track experiment.
* ```mlflow.set_tag("developer", "dev_name")```: to set tags for searching of runs
* ```mlflow.log_param("param_name", param)```: to set parameters to be logged with each run
* ```mlflow.log_metric("rmse", rmse)```: to log metrics
* ```mlflow.log_artifact("path/to/file"-or-object, artifact_path="models/")```: logging anything not metadata or csv, e,g, model pickel, or xgboost objects.

Then just start UI to see runs, use sorting to check best one, or tags for searching, or visualize the runs.

### Autolog in MLflow
For specific models, such as pytorch, tensorflow, keras, xgboost, etc. can use autolog feature of MLflow. Here, instead of manually specifying parameters and metrics, MLflow does it automatically.

## Machine Learning Lifecycle
A picture describing ml engineering. More on it [here](https://neptune.ai/blog/ml-experiment-tracking).
![MLops lifecycle](../images/MLOps_cycle.webp)

## Model Registry

Until now, we worked with MLflow tracking server which stored information about different runs in the experiment, and it is mostly used for designing and model selection. After a model gets ready for production and deployment, the *MLflow model registry* keeps track of the production ready models. It doesn't deploy, but just tracks a list of production ready models.

Need ```from mlflow.tracking import MlflowClient```. This client object has several methods to search, and choose specific runs programmatically. For minimal example look [here](../hw02-experiment-tracking/register_model.py).

