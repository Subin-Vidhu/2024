"""Package a machine learning model
In this exercise, you will train a LinearRegression model from scikit-learn to predict profit of a Unicorn Company.

You will use MLflow's built-in scikit-learn Flavor to package the model. You will use the Flavor's auto logging function to automatically log metrics, parameters and the model to MLflow Tracking when the fit estimator is called."""


# Import Scikit-learn flavor
import mlflow.sklearn

# Set the experiment to "Sklearn Model"
mlflow.set_experiment("Sklearn Model")

# Set Auto logging for Scikit-learn flavor
mlflow.sklearn.autolog()

lr = LinearRegression()
lr.fit(X_train, y_train)

# Get a prediction from test data
print(lr.predict(X_test.iloc[[5]]))

"""Saving and loading a model
With the Model API, models can be shared between developers who may not have access to the same MLflow Tracking server by using a local filesystem.

In this exercise, you will train a new LinearRegression model from an existing one using the Unicorn dataset. First, you will load an existing model from the local filesystem. Then you will train a new model from the existing model and save it back to the local filesystem.

The existing model has been saved to the local filesystem in a directory called "lr_local_v1". The mlflow module will be imported."""

# Load model from local filesystem
model = mlflow.sklearn.load_model("lr_local_v1")

# Training Data
X = df[["R&D Spend", "Administration", "Marketing Spend", "State"]]
y = df[["Profit"]]
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7,random_state=0)
# Train Model
model.fit(X_train, y_train)

# Save model to local filesystem
mlflow.sklearn.save_model(model, "lr_local_v2")

"""Logging and loading a model
The Model API provides a way to interact with our models by logging and loading them directly from MLflow Tracking in a standardized manner. Being able to interact with models is crucial during the ML lifecycle for the Model Engineering and Model Evaluation steps.

In this exercise you will create a Linear Regression model from scikit-learn using the Unicorn dataset. This model will be logged to MLflow Tracking and then loaded using the run_id used to log the artifact.

First, you will log the model using the scikit-learn library from the MLflow module. Then you will load the model from MLflow Tracking using the run_id.

The model will be trained and have the name lr_model.

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
The mlflow module will be imported."""

# Log model to MLflow Tracking
mlflow.sklearn.log_model(lr_model, "lr_tracking")

# Get the last run
run = mlflow.last_active_run()

# Get the run_id of the above run
run_id = run.info.run_id

# Load model from MLflow Tracking run_id and path used to log model
model = mlflow.sklearn.load_model(f"runs:/{run_id}/lr_tracking")

"""Creating a custom Python Class
MLflow provides a way to create custom models in order to provide a way to support a wide variety of use cases. To create custom models, MLflow allows for users to create a Python Class which inherits mlflow.pyfunc.PythonModel Class. The PythonModel Class provides customization by providing methods for custom inference logic and artifact dependencies.

In this exercise, you will create a new Python Class for a custom model that loads a specific model and then decodes labels after inference. The mlflow module will be imported."""

# Create Python Class
class CustomPredict(mlflow.pyfunc.PythonModel):
    # Method for loading model
    def load_context(self, context):
        self.model = mlflow.sklearn.load_model("./lr_model/")
    # Method for custom inference    
    def predict(self, context, model_input):
        predictions = self.model.predict(model_input)
        decoded_predictions = []  
        for prediction in predictions:
            if prediction == 0:
                decoded_predictions.append("female")
            else:
                decoded_predictions.append("male")
        return decoded_predictions

"""Custom scikit-learn model
In this exercise you are going to create a custom model using MLflow's pyfunc flavor. Using the insurance_charges dataset, the labels must be changed from female to 0 and male to 1 for classification during training. When using the model, the strings of female or male must be returned instead of 0 or 1.

The custom model is a Classification model based on LogisticRegression and will use a Class called CustomPredict. The CustomPredict adds an additional step in the predict method that sets your labels of 0 and 1 back to female and male when the model receives input. You will be using pyfunc flavor for logging and loading your model.

Our insurance_charges dataset will be preprocessed and model will be trained using:

lr_model = LogisticRegression().fit(X_train, y_train)
The MLflow module will be imported."""        

# Log the pyfunc model 
mlflow.pyfunc.log_model(
	artifact_path="lr_pyfunc", 
  	# Set model to use CustomPredict Class
	python_model=CustomPredict(), 
	artifacts={"lr_model": "lr_model"}
)

run = mlflow.last_active_run()
run_id = run.info.run_id

# Load the model in python_function format
loaded_model = mlflow.pyfunc.load_model(f"runs:/{run_id}/lr_pyfunc")


"""Scikit-learn flavor and evaluation
In this exercise you will train a classification model and evaluates its performance. The model uses your Insurance Charges dataset in order to classify if the charges were for a female or male.

We will start by logging our model to MLflow Tracking using the scikit-learn flavor and finish by evaluating your model using an eval_data dataset.

Your evaluation dataset is created as eval_data and our model trained with the name lr_class. The eval_data will consist of X_test and y_test as the training data was split using train_test_split() function from sklearn.

# Model
lr_class = LogisticRegression()
lr_class.fit(X_train, y_train)
The mlflow module is imported."""

# Eval Data
eval_data = X_test
eval_data["sex"] = y_test
# Log the model using Scikit-Learn Flavor
mlflow.sklearn.log_model(lr_class, "model")

# Get run id
run = mlflow.last_active_run()
run_id = run.info.run_id

# Evaluate the logged model with eval_data data
mlflow.evaluate(f"runs:/{run_id}/model", 
                data=eval_data, 
                targets="sex",
				model_type="classifier"
)

