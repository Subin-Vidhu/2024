# Workout Tracker

## Objective

Build an exercise tracking app using natural language processing and Google sheets.

You **won't** be able to run this solution code as is. Why? You'll need to add **your own** API keys as environment variables first.

## PyCharm Environment Variables

In PyCharm you set your environment variables under "Edit Configurations". You should see a section called "Environment" -> "Environment Variables". There, you can click a small symbol which brings up a window where you can paste all your environment variables at the same time. The format follows the example of the env_for_pycharm file (use your own API keys)

## Replit Environment Variables

For Replit you need to click on the padlock symbol (Secrets) in the menu. There you can add your environment variables. You can either add them one by one or paste them from a .json file. The .json provided is just an example. You'll need to replace it with own API keys.

## FAQ KeyError

The name of your environment variables in your Python code needs to match what your environment variables are actually called. If you use:

```
API_KEY = os.environ["NT_API_KEY"]
```

Then make sure your environment variable is actually called `NT_API_KEY`. If you use a different name (like `ENV_NIX_API_KEY`) then make sure your Python code matches.

## FAQ Sheety: Insufficient Permission

Sheety needs permission to access your Google Sheet. When you sign into Sheety you probably forgot to give it permission. Sign out of Sheety and sign in again. Also, go to your Google Account -> Security -> Third Party Apps with Account Access. Check that you see Sheety listed there.

## FAQ Sheety: Bad Request. The JSON Payload should be inside a root property called "X"

Your Google sheet's name should be plural – if it isn’t then Sheety will still expect it to be camelCase plural in the API endpoint. i.e. if your sheet is named "My Workouts", then you should use "myWorkouts" in your endpoint.
The Project name in the endpoint must also be camelCase.
The name you use for the primary key in the API call should be the camelCase singular version of the sheet name. i.e. if your sheet is named "My Workouts", then you should use "myWorkout" in your API dictionary. You may also need to refresh the API page on Sheety.
