import csv

def calculate_mean_dice_scores(csv_file_path):
    """Read the CSV file and calculate the mean Dice score for each class."""
    with open(csv_file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        # Initialize a dictionary to store the sum of Dice scores for each class
        class_scores_sum = {class_name: 0.0 for class_name in header[1:]}
        num_cases = 0
        
        # Read the Dice scores for each case
        for row in reader:
            num_cases += 1
            for class_name, score in zip(header[1:], row[1:]):
                class_scores_sum[class_name] += float(score)
        
        # Calculate the mean Dice score for each class
        mean_dice_scores = {class_name: score_sum / num_cases for class_name, score_sum in class_scores_sum.items()}
        
        return mean_dice_scores

# Path to the CSV file
csv_file_path = r'D:\2024\zTest\dice_scores.csv'

# Calculate the mean Dice scores
mean_dice_scores = calculate_mean_dice_scores(csv_file_path)

# Print the mean Dice scores
for class_name, mean_score in mean_dice_scores.items():
    print(f'Mean Dice Score for {class_name}: {mean_score:.4f}')
# def calculate_mean_dice_scores(csv_file_path):
#     """Read the CSV file and calculate the mean Dice score for each class."""
#     with open(csv_file_path, mode='r') as file:
#         reader = csv.reader(file)
#         header = next(reader)
        
#         # Initialize a dictionary to store the sum of Dice scores for each class
#         class_scores_sum = {class_name: 0.0 for class_name in header[1:]}
#         num_cases = 0
        
#         # Read the Dice scores for each case
#         for row in reader:
#             num_cases += 1
#             for class_name, score in zip(header[1:], row[1:]):
#                 class_scores_sum[class_name] += float(score)
        
#         # Calculate the mean Dice score for each class
#         mean_dice_scores = {class_name: score_sum / num_cases for class_name, score_sum in class_scores_sum.items()}
        
#         return mean_dice_scores

# # Path to the CSV file
# csv_file_path = r'D:\2024\zTest\dice_scores.csv'

# # Calculate the mean Dice scores
# mean_dice_scores = calculate_mean_dice_scores(csv_file_path)

# # Print the mean Dice scores
# for class_name, mean_score in mean_dice_scores.items():
#     print(f'Mean Dice Score for {class_name}: {mean_score:.4f}')
