import json  # Import the json module to work with JSON files

# Open the nutrition.json file in read mode and load its content into a dictionary
with open('nutrition.json', 'r') as json_file:
    nutrition_dict = json.load(json_file)  # Load the JSON content into a dictionary
    
# Display the first 3 items of the nutrition dictionary
list(nutrition_dict.items())[:3]

# Define a function to calculate the nutritional summary given a dictionary of foods and their weights
def nutritional_summary(foods):
    # Initialize result dictionary to store total nutritional values
    result_dict = {"calories": 0, "total_fat": 0, "protein": 0, "carbohydrate": 0, "sugars": 0} 
    
    # Process each food item
    for name, grams in foods.items():
        if name in nutrition_dict:
            # Get the nutritional information for the food item
            nutrition = nutrition_dict[name]
            # Calculate and add the nutritional values based on the given weight (grams)
            result_dict["calories"] += grams * nutrition["calories"] / 100
            result_dict["total_fat"] += grams * nutrition["total_fat"] / 100
            result_dict["protein"] += grams * nutrition["protein"] / 100
            result_dict["carbohydrate"] += grams * nutrition["carbohydrate"] / 100
            result_dict["sugars"] += grams * nutrition["sugars"] / 100
        else:
            # Return the name of the first food item not found in the nutrition_dict
            return name
    # Return the total nutritional values
    return result_dict

# Calling the function and checking the output
print(nutritional_summary({"Croissants, cheese": 150, "Orange juice, raw": 250}))
print(nutritional_summary({"Croissant": 150, "Orange juice": 250}))