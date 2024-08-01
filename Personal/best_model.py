import pandas as pd
import numpy as np

# Define constants
METRICS = ['accuracy', 'f1-score', 'iou_score', 'loss', 'val_accuracy', 'val_f1-score', 'val_iou_score', 'val_loss']
WEIGHTS = {
    'accuracy': 0.1,
    'f1-score': 0.3,
    'iou_score': 0.5,
    'loss': -0.1,
    'val_accuracy': 0.05,
    'val_f1-score': 0.15,
    'val_iou_score': 0.25,
    'val_loss': -0.05
}

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
    composite_score = calculate_composite_score(df, WEIGHTS)
    top_models = select_best_models(df, composite_score)
    return top_models

# Load the CSV file into a DataFrame
df = pd.read_csv(r"g:\VERTEBRAE_MODELS\75_cases\my_logs.csv")

# Evaluate the models
top_models = evaluate_models(df)

# Print the top 10 models
print("Top 10 Models:")
print(top_models)
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