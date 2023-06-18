# MLOps Zoomcamp journey
Notes, homeworks, and projects for [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp).

## Links

* [Notes](./notes/)
* [hw02](./hw02-experiment-tracking/): using MLflow to set experiment tracking with a data backend, setting tags, logging parameters; Tracking example with hyperparameter optimization using optuna [here](./hw02-experiment-tracking/hpo.py); Programmatic model registry as shown [here](./hw02-experiment-tracking/register_model.py).
* [hw03](./hw03-orchestration/): using Prefect to orchestrate flows and tasks programmatically. basically use prefect @flow and @task decorators to define an orchestration entrypoint. Now a UI or other ways e.g. CLI can be used to define a workpool to be used as compute nodes to run different jobs for example periodically run a task. Also can be used to send results via email, but many other orchestration options available as part of the prefect package. Minimal code example can be found in [here](./hw03-orchestration/orchestrate.py), make sure to have additional setups already running such as backend server (local or remote), a pool of workers, and can populate tasks to be run.
* [hw04](./hw04-deployment/)