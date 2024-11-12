"""MLflow experiments
MLflow experiments are used as a way to organize data from training runs in a way that can be easily searched and queried for our analysis later.

In this exercise, you will use the MLflow module to create a new experiment called Unicorn Model for your new ML project. You will add useful information to the experiment by setting tags for the version. Finally, you will set the Unicorn Model experiment as your current experiment so when you begin tracking your data will be tracked within this particular experiment.
"""

# Import MLflow
import mlflow

# Create new experiment
mlflow.create_experiment("Unicorn Model")

# Tag new experiment
mlflow.set_experiment_tag("version", "1.0")

# Set the experiment
mlflow.set_experiment("Unicorn Model")

"""Starting a run
MLflow uses the concept of a run as a way to organize model training. Before metrics, parameters or artifacts can be logged to MLflow Tracking, a run must become active. Each run must also belong to an existing experiment.

In the following exercise, you will start a new run so that you can begin logging a model. You will also set the experiment in which you would like the run to be logged. The mlflow module will already be imported for you."""

# Set the experiment
mlflow.set_experiment("Unicorn Sklearn Experiment")

# Start a run
mlflow.start_run()

"""Logging a run
In this exercise, you will train a model using scikit-learn's Linear Regression to predict profit from the Unicorn dataset. You have created an experiment called Unicorn Sklearn Experiment and started a new run. You will log metrics for r2_score and parameters for n_jobs as well as log the training code as an artifact.

The Linear Regression model will be trained with n_jobs parameter set to 1. The r2_score metric has been produced using the r2_score() from scikit-learn based on y_pred variable which came from predictions of X_test.

model = LinearRegression(n_jobs=1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

r2_score = r2_score(y_test, y_pred)
The mlflow module as well as the LinearRegression, train_test_split, and metrics modules from scikit-learn will be imported."""

# Log metrics
mlflow.log_metric("r2_score", r2_score)

# Log parameter
mlflow.log_param("n_jobs", n_jobs)

# Log the training code
mlflow.log_artifact("train.py")

"""How to retrieve active run data?
MLflow uses the concept of runs to log metrics, parameters and artifacts to MLflow Tracking. Using the start_run() function from the mlflow module starts a new run and sets it to an active state. This is helpful if information such as run_id or artifact_uri needs to be retrieved.

A run has been set to active using the following code:

run = mlflow.start_run()"""

"""Searching runs
In this exercise, you will query experiment runs from multiple Unicorn experiments and return only runs that meet a certain desired criteria. This is helpful during the ML lifecycle if you need to compare runs data.

First you will create a filter string to capture runs for R-squared metric greater than .70. Using the function from the mlflow module that searches runs, you will then order them in descending order and search only the experiments "Unicorn Sklearn Experiments" and "Unicorn Other Experiments".

The experiments have already been created in MLflow along with the R-squared metrics. The MLflow module will be imported."""

# Create a filter string for R-squared score
r_squared_filter = "metrics.r2_score > .70"

# Search runs
mlflow.search_runs(experiment_names=["Unicorn Sklearn Experiments", "Unicorn Other Experiments"], 
                   filter_string=r_squared_filter, 
                   order_by=["metrics.r2_score DESC"])

                   