"""Create a Model
The MLflow Model Registry provides a centralized storage location for MLflow Models. The Registry enables collaboration and provides a way to manage a model's lifecycle.

In this exercise, you will use the mlflow client module to create a new Model named "Insurance". This will create an area in the MLflow Model Registry where you can register versioned models at a later time."""

# Import MLflow Client from MLflow module
from mlflow import MlflowClient

# Create an instance of MLflow Client Class name client
client = MlflowClient()

# Create new model
client.create_registered_model("Insurance")

"""Searching Models
As the MLFlow Model Registry grows and you collaborate with other users, you need to be able to search the Model Registry for models that fit certain criteria.

In this exercise, you will create two filter strings to search the MLflow Model Registry for Models. The first filter string searches for all "Insurance" Models and the second filter string searches Non-"Insurance" Models.

Models have already been created by other collaborators using the same MLflow Model Registry and an instance of the MLflow Client module will already be set as client.

client = mlflow.MlflowClient()
The MLflow Client module will be imported."""

# Insurance filter string
insurance_filter_string = "name LIKE 'Insurance%'"

# Search for Insurance models
print(client.search_registered_models(filter_string=insurance_filter_string))

# Not Insurance filter string
not_insurance_filter_string = "name != 'Insurance'"

# Search for models that are not Insurance
print(client.search_registered_models(filter_string=not_insurance_filter_string))

"""Registering existing models
In this exercise, you will take two existing MLflow Models and register them to the MLflow Model Registry to begin managing the lifecycle of both models. Each of these models was trained using the "Insurance" data at a previous date to predict if an insurance claim was for a male or female.

The first model can be found in the local directory "model_2022" and was never logged to MLflow Tracking. The second model was logged to MLflow Tracking under the artifact URI of "model_2023". Its run_id attribute has been saved as a variable named "run_id".

The mlflow module will be imported."""

# Register the first (2022) model
mlflow.register_model("model_2022", "Insurance")

# Register the second (2023) model
mlflow.register_model(f"runs:/{run_id}/model_2023", "Insurance")

"""Registering new models
The MLflow Model Registry can also register models during a training run. This is helpful because it enables logging and registering a model under the same function.

In this exercise, you will use the scikit-learn flavor to register a model to the Model Registry during a training run when the model is logged to MLflow Tracking. You will then search the Model Registry to ensure the model was registered.

This model will be registered alongside existing registered models that were trained on the "Insurance" training data. The model has already been trained and set to the variable lr. When searching the Model Registry, an instance of MLflowClient() has been set to client and the filter string has already been created as insurance_filter_string."""

# Log the model using scikit-learn flavor
mlflow.sklearn.log_model(lr, "model", registered_model_name="Insurance")
insurance_filter_string = "name = 'Insurance'"

# Search for Insurance models
print(client.search_registered_models(filter_string=insurance_filter_string))

"""Transitioning model stages
Once models are registered to the Model Registry, each model version is eligible for a stage assignment. Stages are used to manage the model lifecycle and are used to represent different development environments.

In this exercise, using the mlflow client Class as client, you will take your "Insurance" models and transition each model according to the stage in your development lifecycle. First, you will transition your most stable model for production use. Then you will transition to a model that needs testing and evaluation. Finally, you will archive a model that is no longer needed.

The mlflow client module will be imported."""

# Transition version 1 of Insurance model to archive stage
client.transition_model_version_stage(name="Insurance", version=1,
        stage="Archived"
    )


"""Loading models from the Model Registry
In this exercise, you will use the scikit-learn flavor to deploy the most stable "Insurance" model from the MLflow Model Registry and then use test data to get a prediction from the model.

The model uses LogisticRegression to predict whether an insurance claim is for a male or female, which is labeled as 1 or 0. You'll load the model and then make predictions using a test set called X_test.

The MLflow module will be imported."""

# Load the Production stage of Insurance model using scikit-learn flavor
model = mlflow.sklearn.load_model("models:/Insurance/Production")

# Run prediction on our test data
model.predict(X_test)                          

