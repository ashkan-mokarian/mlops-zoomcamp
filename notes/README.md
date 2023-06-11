# Notes
Minimal personal notes along the way.

# TOC

* [Experiment Tracking](#experiment-tracking): definition and goals; MLflow;
* [Orchestration](#orchestration): using Prefect here; Tasks and Flows in Prefect;

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

# Orchestration

### Tasks
Python function decorated with @task from Prefect. A unit of work in a prefect workflow.

### Flow
Also py function decorated with @flow. Container for workflow logic. Flows can also call other flows termed subflows.

Similar to other workflow management systems, first run the server using ```prefect server start```. This open an API server node to interact with the server during your runs. After that, a message appears starting with ```prefect config set ...```, run it in another terminal to set the config of api for the server in it. In this terminal, you can run python files decorated with flow and task, in order to interact with the prefect backend server. The results can be viewed in the UI and explored accordingly.

## Deployment

First create a prefect project in the project directory using ```prefect project init```. This will create files project.yaml and deployment.yaml

Next create a worker pool, either using cli or the UI. I think this defines some resources to be used to run flows on the from a pool of tasks. It can be a process on a local machine or other remote ones.

Then run the local server or connect to a remote server.

deploy the flow entrypoint to the server as ```prefect deploy my-flow.py:entry-point[this is the function name entry point for the flow] -n "deployment name" -p worker-pool-name```

Start a run by ```prefect deployment run flow-name/deployment-name```

This workflow clones from a remote repo. So make sure to have the data included in your repo. Moreover, apparently, it assumes the cwd to be the root of the repo. These comments are for the case where the deployment settings are left without any changes. You can probably change them to your specific need, but here we just used the default settings.


