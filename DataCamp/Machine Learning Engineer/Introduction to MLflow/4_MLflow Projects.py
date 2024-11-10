"""Creating an MLproject
An MLproject file is a yaml file that stores the configuration of an MLflow Project. The file defines information such as name of the Project, Python environment and entry points to be executed as part of a workflow.

In this exercise, you will create an MLproject file to describe an MLflow Project. You will define the name of the Project, the Python environment, and also create an entry point."""

"""
# Set name of the Project
name: insurance_model

# Set the environment
python_env: python_env.yaml

entry_points:
 	# Create an entry point
 	main:
   		# Create a command
    	command: 'python3.9 train_model.py'
"""

"""MLflow projects module
MLflow Projects can also be run programmatically with Python using the mlflow projects module.

In this exercise you will run an MLflow Project using the projects module to train a model for your "Insurance" Project. You will define the entry point from your MLproject file to execute the training code. You will also define the experiment name of "Insurance" so that the model is properly logged to the correct experiment in MLflow Tracking.

You may read the contents of the MLproject file by executing print(MLproject) in the IPython shell."""

import mlflow

# Set the run function from the MLflow Projects module
mlflow.projects.run(
    # Set the URI as the current working directory
    uri='./',
    # Set the entry point as main
    entry_point='main',
    # Set the experiment as Insurance
    experiment_name='Insurance',
    env_manager="local",
    synchronous=True,
)

"""Adding parameters to MLproject
Defining parameters in MLflow Projects allows you to make your ML code reproducible. Parameters also simplify running training experiments with different settings without having to change code.

In this exercise, you are going to add parameters to your MLproject file for the main entry point. This entry point is used to run the train_model.py script which trains a Logistic Regression model from Insurance data.

The script accepts two parameters, n_jobs and fit_intercept, which are hyperparameters used to train the model. You will begin by adding the n_jobs parameter in the MLproject file. You will then add the fit_intercept parameter. Finally, you will add the parameters to the command executed in the main entry point."""

"""
name: insurance_model
python_env: python_env.yaml
entry_points:
  main:
    parameters:
      # Create parameter for number of jobs
      n_jobs:
        type: int
        default: 1
      # Create parameter for fit intercept
      fit_intercept:
        type: bool
        default: True
    # Add parameters to be passed into the command
    command: "python3.9 train_model.py {n_jobs} {fit_intercept}"
"""

"""Adding parameters to project run
Parameters can be used to configure the behavior of a model by being passed as variables to the model during training. This allows you to train the model several times using different parameters without modifying the training code itself.

In this exercise, you will use the mlflow projects module to run a Project used to train a Logistic Regression model for your Insurance experiment. You will create code using the mlflow projects module that will run your project. You will then add parameters that will be passed as hyperparameters to the model during training.

"""

import mlflow

# Set the run function from the MLflow Projects module
mlflow.projects.run(
    uri='./',
    entry_point='main',
    experiment_name='Insurance',
  	env_manager='local',
  	# Set parameters for n_jobs and fit_intercept
  	parameters={
        'n_jobs_param': 2, 
        'fit_intercept_param': False
    }
)

"""Creating an MLproject for the ML Lifecycle: Model Engineering
The MLproject file can include more than one entry point. This means that you can use a single MLproject file to execute multiple entry points, making it possible to execute a workflow of multiple steps using a single MLproject file.

In this exercise you are going to build the beginning of an MLproject file that contains the model_engineering entry point. This entry point will execute a python script that accepts parameters used as hyperparameter values for fit_intercept and n_jobs to a Logistic Regression model. This model is used to predict sex of person from an insurance claim."""

"""
name: insurance_model
python_env: python_env.yaml
entry_points:
  # Set the entry point
  model_engineering:
    parameters: 
      # Set n_jobs 
      n_jobs:
        type: int
        default: 1
      # Set fit_intercept
      fit_intercept:
        type: bool
        default: True
    # Pass the parameters to the command
    command: "python3.9 train_model.py {n_jobs} {fit_intercept}"
"""

"""Creating an MLproject for the ML Lifecycle: Model Evaluation
In this exercise, you will continue creating your MLproject file to manage steps of the ML lifecycle. You will create another entry point called model_evaluation. This step in the workflow accepts the run_id output from the model_engineering step and runs model evaluation using training data from our Insurance dataset.

You can print the current MLproject file using the IPython Shell and executing print(MLproject)."""


"""
  # Set the model_evaluation entry point
  model_evaluation:
    parameters:
      # Set run_id parameter
      run_id:
        type: str 
        default: None
    # Set the parameters in the command
    command: "python3.9 evaluate.py {run_id}"
"""


"""Creating a multi-step workflow: Model Engineering
The MLflow Projects module can be used as a way to run a multi-step workflow. All steps can be coordinated though a single Python program that passes results from previous steps to the following.

In this exercise, you will begin creating a multi-step workflow to manage the Model Engineering and Model Evaluation steps of the ML lifecycle. You will use the run() method from the MLflow Projects module for the model_engineering entry point and pass parameters used as hyperparameters for model training. You will also capture the output of the run_id and set it to a variable so that it can be passed to the model_evaluation step of the workflow as a parameter.

The MLproject created in the previous step is available in the IPython Shell using print(MLproject). The MLflow module is imported."""

# Set run method to model_engineering
model_engineering = mlflow.projects.run(
    uri='./',
  	# Set entry point to model_engineering
    entry_point='model_engineering',
    experiment_name='Insurance',
    #  Set the parameters for n_jobs and fit_intercept
  	parameters={
        'n_jobs': 2, 
        'fit_intercept': False
    },
    env_manager='local'
)

# Set Run ID of model training to be passed to Model Evaluation step
model_engineering_run_id = model_engineering.run_id
print(model_engineering_run_id)

"""Creating a multi-step workflow: Model Evaluation
In this exercise, you will create the Model Evaluation step of our multi-step workflow used to manage part of the ML lifecycle. You will use the run() method from the MLflow Projects module and set the entry point to model_evaluation. You will then take the model_engineering_run_id as a parameter that was generated as an output in the previous exercise and pass it to the command.

The MLproject created in the previous step is available in the IPython Shell using print(MLproject).

The mlflow module is imported."""

# Set the MLflow Projects run method
model_evaluation = mlflow.projects.run(
    uri="./",
  	# Set the entry point to model_evaluation
    entry_point="model_evaluation",
  	# Set the parameter run_id to the run_id output of previous step
    parameters={
        "run_id": model_engineering_run_id,
    },
    env_manager="local"
)

print(model_evaluation.get_status())

