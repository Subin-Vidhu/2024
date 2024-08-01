import pandas as pd
import numpy as np

# Define constants
METRICS = ['accuracy', 'f1-score', 'iou_score', 'loss', 'val_accuracy', 'val_f1-score', 'val_iou_score', 'val_loss']

def calculate_best_metric_weights(df, metrics):
    """Calculate the best metric weights based on the maximum value in each column"""
    weights = {}
    for metric in metrics:
        if metric in df.columns:
            max_value = df[metric].max()
            if metric.startswith('val_'):
                weights[metric] = max_value / 2  # reduce weight for validation metrics
            else:
                weights[metric] = max_value
        else:
            raise ValueError(f"Missing column: {metric}")
    return weights

'''
The dynamic weights approach I proposed has several advantages over the hardcoded weights approach:
Adaptability: By calculating the weights based on the maximum value in each column, the model can adapt to the specific characteristics of the data. This is particularly useful when working with different datasets or models, where the importance of each metric may vary.
Flexibility: The dynamic weights approach allows for easy incorporation of new metrics or changes to the existing metrics. You don't need to manually update the weights; the model will automatically adjust to the new metrics.
Robustness: Hardcoded weights can be sensitive to outliers or anomalies in the data. By using the maximum value in each column, the dynamic weights approach is more robust to these issues.
Interpretability: The dynamic weights approach provides a clear understanding of the importance of each metric in the composite score. You can see which metrics are driving the composite score and adjust the model accordingly.
Reduced bias: By letting the data determine the weights, you reduce the risk of introducing bias through manual weight selection.
Improved generalizability: The dynamic weights approach can lead to better generalizability of the model, as it's not tied to specific weights that might not be applicable to new, unseen data.
In contrast, hardcoded weights can:
Introduce bias: Manual weight selection can introduce bias, as the weights may not accurately reflect the importance of each metric.
Be inflexible: Hardcoded weights can make it difficult to incorporate new metrics or changes to the existing metrics.
Be sensitive to outliers: Hardcoded weights can be sensitive to outliers or anomalies in the data, which can affect the model's performance.
Overall, the dynamic weights approach provides a more flexible, adaptable, and robust way to calculate the composite score, which can lead to better model performance and interpretability.
'''
def calculate_composite_score(df, weights):
    """Calculate the composite score for each row (model)"""
    composite_score = np.zeros(len(df))
    for metric, weight in weights.items():
        if metric in df.columns:
            composite_score += weight * df[metric]
        else:
            raise ValueError(f"Missing column: {metric}")
    return composite_score

def select_best_models(df, composite_score, n=10):
    """Select the top N models based on the composite score"""
    top_model_indices = np.argsort(composite_score)[::-1][:n]
    return df.iloc[top_model_indices]

def evaluate_models(df):
    """Evaluate the models based on the composite score"""
    weights = calculate_best_metric_weights(df, METRICS)
    composite_score = calculate_composite_score(df, weights)
    top_model_indices = np.argsort(composite_score)[::-1]
    top_models = df.iloc[top_model_indices]
    top_models['composite_score'] = composite_score[top_model_indices]
    return top_models

# Load the CSV file into a DataFrame
df = pd.read_csv(r"d:\PROTOS\VERTEBRAE\Training_Codes\models\75_cases_val_loss\my_logs.csv")

# Evaluate the models
top_models = evaluate_models(df)

# Print the top 10 models with their composite scores
print("Top 10 Models:")
print(top_models.head(10))

# import pandas as pd
# import numpy as np

# # Define constants
# METRICS = ['accuracy', 'f1-score', 'iou_score', 'loss', 'val_accuracy', 'val_f1-score', 'val_iou_score', 'val_loss']
# WEIGHTS = {
#     'accuracy': 0.1,
#     'f1-score': 0.3,
#     'iou_score': 0.5,
#     'loss': -0.1,
#     'val_accuracy': 0.05,
#     'val_f1-score': 0.15,
#     'val_iou_score': 0.25,
#     'val_loss': -0.05
# }

# def calculate_composite_score(df, weights):
#     """Calculate the composite score for each row (model)"""
#     composite_score = np.zeros(len(df))
#     for metric, weight in weights.items():
#         if metric in df.columns:
#             composite_score += weight * df[metric]
#         else:
#             raise ValueError(f"Missing column: {metric}")
#     return composite_score

# def select_best_models(df, composite_score, n=10):
#     """Select the top N models based on the composite score"""
#     top_model_indices = np.argsort(composite_score)[::-1][:n]
#     return df.iloc[top_model_indices]

# def evaluate_models(df):
#     """Evaluate the models based on the composite score"""
#     composite_score = calculate_composite_score(df, WEIGHTS)
#     top_models = select_best_models(df, composite_score)
#     return top_models

# # Load the CSV file into a DataFrame
# df = pd.read_csv(r"g:\VERTEBRAE_MODELS\75_cases\my_logs.csv")

# # Evaluate the models
# top_models = evaluate_models(df)

# # Print the top 10 models
# print("Top 10 Models:")
# print(top_models)


# # deepseek
# import pandas as pd
# import numpy as np

# # Load the CSV file into a DataFrame
# df = pd.read_csv(r"g:\VERTEBRAE_MODELS\75_cases\my_logs.csv")

# # Normalize the metrics
# def normalize(df, columns):
#     for col in columns:
#         df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
#     return df

# metrics = ["accuracy", "f1-score", "iou_score", "loss", "val_accuracy", "val_f1-score", "val_iou_score", "val_loss"]
# df = normalize(df, metrics)

# # Define weights for each metric (you can adjust these based on importance)
# weights = {
#     "accuracy": 0.1,
#     "f1-score": 0.3,
#     "iou_score": 0.5,
#     "loss": -0.1,
#     "val_accuracy": 0.05,
#     "val_f1-score": 0.15,
#     "val_iou_score": 0.25,
#     "val_loss": -0.05
# }

# # Calculate composite score for each row (model)
# df['composite_score'] = (
#     weights['accuracy'] * df['accuracy'] +
#     weights['f1-score'] * df['f1-score'] +
#     weights['iou_score'] * df['iou_score'] +
#     weights['loss'] * df['loss'] +
#     weights['val_accuracy'] * df['val_accuracy'] +
#     weights['val_f1-score'] * df['val_f1-score'] +
#     weights['val_iou_score'] * df['val_iou_score'] +
#     weights['val_loss'] * df['val_loss']
# )

# # Find the row (model) with the highest composite score
# best_model = df.loc[df['composite_score'].idxmax()]

# # Print the best model details
# print("Best Model:")
# print(best_model)







# import pandas as pd
# import numpy as np

# # Load the CSV file into a DataFrame
# df = pd.read_csv(r"g:\VERTEBRAE_MODELS\75_cases\my_logs.csv")
# # df = pd.read_csv(r"D:\PROTOS\AIRA\Results_New\training_logs.csv")

# # # Extract column names
# # columns = df.columns

# # # Initialize a dictionary to store minimum values
# # min_values = {}

# # # Iterate over each column
# # for col in columns:
# #     # Extract values for the column
# #     values = df[col].values
# #     # Find the minimum value
# #     min_value = np.min(values)
# #     # Store the minimum value in the dictionary
# #     min_values[col] = min_value

# # # Print the minimum values for each column
# # print("Minimum values for each column:")
# # for col, min_val in min_values.items():
# #     print(f"{col}: {min_val}")


# # Define weights for each metric (you can adjust these based on importance)
# # weights = {
# #     "accuracy": 0.2,
# #     "f1-score": 0.2,
# #     "iou_score": 0.2,
# #     "loss": -0.2,
# #     "val_accuracy": 0.1,
# #     "val_f1-score": 0.1,
# #     "val_iou_score": 0.1,
# #     "val_loss": -0.1
# # }
# weights = {
#     "accuracy": 0.1,
#     "f1-score": 0.3,
#     "iou_score": 0.5,
#     "loss": -0.1,
#     "val_accuracy": 0.05,
#     "val_f1-score": 0.15,
#     "val_iou_score": 0.25,
#     "val_loss": -0.05
# }
# # Calculate composite score for each row (model)
# df['composite_score'] = (
#     weights['accuracy'] * df['accuracy'] +
#     weights['f1-score'] * df['f1-score'] +
#     weights['iou_score'] * df['iou_score'] +
#     weights['loss'] * df['loss'] +
#     weights['val_accuracy'] * df['val_accuracy'] +
#     weights['val_f1-score'] * df['val_f1-score'] +
#     weights['val_iou_score'] * df['val_iou_score'] +
#     weights['val_loss'] * df['val_loss']
# )

# # Find the row (model) with the highest composite score
# best_model = df.loc[df['composite_score'].idxmax()]

# # Print the best model details
# print("Best Model:")
# print(best_model)