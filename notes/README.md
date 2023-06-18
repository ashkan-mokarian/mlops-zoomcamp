# Notes
Minimal personal notes along the way.

# TOC

* [Experiment Tracking](#experiment-tracking): definition and goals; MLflow;
* [Orchestration](#orchestration): using Prefect here; Tasks and Flows in Prefect;
* [Deployment]

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

## Deploy Orchestration workflows

First create a prefect project in the project directory using ```prefect project init```. This will create files project.yaml and deployment.yaml

Next create a worker pool, either using cli or the UI. I think this defines some resources to be used to run flows on the from a pool of tasks. It can be a process on a local machine or other remote ones.

Then run the local server or connect to a remote server.

deploy the flow entrypoint to the server as ```prefect deploy my-flow.py:entry-point[this is the function name entry point for the flow] -n "deployment name" -p worker-pool-name```

Start a run by ```prefect deployment run flow-name/deployment-name```

This workflow clones from a remote repo. So make sure to have the data included in your repo. Moreover, apparently, it assumes the cwd to be the root of the repo. These comments are for the case where the deployment settings are left without any changes. You can probably change them to your specific need, but here we just used the default settings.


# Deployment

During the last weeks, we went through the steps of designing and experimenting with models to choose a model ready for production. Here, we want to take this model and deploy it for predictions. Different ways are available here:

* Batch/Offline: We don't need the results immediately and we can wait for some time.
* Online: Up an running all the time. It's always available.
    * Web Service: We can send http requests
    * Streaming: Model service is listening and ready to response

### Batch model
Run the mode regularly in time intervals (hours, days, weeks). Here we have a dataset which we put our fresh data in. And there is a scoring/prediction job that pulls data from the database and makes the predictions on it. If it is scheduled daily, it pulls all data from the last daya for example. We write the results of this batch run to another place, e.g. another database. Results are now available to be used, for example to create a report about the last day data. Use case: Marketing related tasks, Churn (when customers leave our service and we want to give incentives for the returning) here we need to do churn daily or even weekly to recognize churning. For this you will create a churn scoring job model, pull data of last week and reason about customer change behaviour and creates a database of users churning. Then another job can pull these results and for example send push notifications to them with incentives. This is not a job requiring to be run all the time, but only regularly.

### Web Service
Here the model is available all the time since user wants ride duration results on the app immediately. For example for our taxi service, we have a user requesting a taxi, the backend of the app send relevant information such as user id, pick up location, etc to the 'Ride Duration Service' model and the model makes predictions and sends it back to the backend. Here the connection stays alive for the duration of getting back the results from the model, and this is what distinguishes Web Service deployment from Streaming.

### Streaming
Here it is one-to-many connection and involvles a producer and many services. For our example of taxi service, the user interacts with the app and sends info to the backend. Now the backend might connect to a WebService model to get a quick ride duration prediction results for the ride. But this backend can also act as a producer and send the ride informations to many services, but does not necessarily wait for a response from them. Now each service can decide to run a task and do something with this information. For example one can be a more accurate ride duration prediction that gives a more accurate result when the ride has already started. Another could be a tip prediction model and send a push notification to the user about the amount to tip. In Streaming, we know that there are some services using the information sent to them to do something with it, but we don't know who, how many, and how long it will take, and if they are reacting to it or not and as far as backend is concerned, he just pushes the ride data to the services. A more realisitc usecase: On youtube, a user creates a video, and a service can look for copyright, one for NSFW, violence, ... . Here the work of the producer is done and rest is left to the rest.

## Deploying steps
For this module, the entry point is the best model pickeled files from previous modules, i.e. the DictionaryVectorizer and the sklearn pickled model.

### Deployment as a Web Service
Steps:

1. Choose the exact version of the sklearn for the pickled files. And create a pipenv environment with the packages required, here the exact version of scikit-learn, flask. Not necessary, but we can also specify the exact python version. All is done by using **pipenv** that creates a virtual environment isolated for the project. The command is `pipenv install scikit-learn==1.0.2 flask --python=3.9`. Then we run (I think in the project folder where we created the pipenv) `pipenv shell` to activate the environment. This has created a 'Pipfile' that specifies requirement of packages and a 'Pipfile.lock' that has the hashes for the exact packages installed.

2. Creating a script for prediction: Here we take the saved model and load it, receive the ride data, do the proper feature transformations, and predict based on the features in a simple predict.py file. 

3. Putting the predict.py in a flask app: Since this is the Web Service, make sure to have a function 'predict_endpoint' that receives the http request of the ride information and returns the jsonify version of result. It is the main function to interact with the backend flask app. So it needs to be decorated with the proper flask decorator, here it was `@app.route('/predict', methods=['POST'])`. In the __main__ section, we add `app.run(debug=True, host='0.0.0.0', port=9696)`. Also need to have `from flask import Flask, requests, jsonify`. For a minimal example of testing it see [here](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/04-deployment/web-service/test.py) and for the main code [here]|(https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/04-deployment/web-service/predict.py)

**Note**: In the above test.py file, we used requests package, but this package is not required for production and we only used it for testing. To install a package marked as development only, use `pipenv install --dev requests` instead. This way, the package will be installed for developers, but not for production.

**Note:** Flask is used for development purposes, and when ran gives a warning to not use a 'WSGI' server instead. For this we install `pipenv install gunicorn`.

4. Packaging the app to Docker: The example is [here](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/04-deployment/web-service/Dockerfile)

**Note**: -slim is used for base docker image, because it is more slim.
**Note**: Since in a docker we are already pretty isolated, when installing packaged we don't want to create a virtual environment but rather install it system-wide, that's why we add '--system'.

#### Serving the registered models from MLflow Model Registry
We already know we can load a model from MLflow as a pythonfunc by giving a RUN_ID, we can also save the vectorizer as an artifact, and then by using client class in MLFlow, access the artifact, download and use it, and hence we can implement the whole web service as before but with automatically looking for models from mlflow model registry. However, there is also an easier way. Instead of having a RadomForest as the model and the DictVectorizer as an artifact, we can use `scikit-learn.PipeLine.MakePipeline` to create a model from to, and register this as the final model, and hence do not need to deal with artifacts. An improvement to this is to use model registry and instead of accessing the mlflow server, to use the actual address of the model (For example in AWS, S3 is more reliable than the mlflow server in EC2). Furthermore, the RUN_ID can be set as an environment variable which could easily be passed in the docker file and kubernets.

### Deployment for Batch scheduled with Prefect
Basically make a script with arguments from CLI, and use scheduling to run.