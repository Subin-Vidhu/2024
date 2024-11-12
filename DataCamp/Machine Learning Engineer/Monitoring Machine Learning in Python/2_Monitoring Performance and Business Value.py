"""Comparing estimated and realized performance
Now that you have seen how performance calculation works, your task is to calculate the realized performance for our tip prediction model for the NYC green taxi dataset.

The reference and analysis set is already loaded and saved in the reference and analysis variables.

In addition, results from the DLE algorithm for tip prediction are stored in the estimated_results variable."""

# Intialize the calculator
calculator = nannyml.PerformanceCalculator(
    y_true='tip_amount',
    y_pred='y_pred',
    chunk_period='d',
  	metrics=['mae'],
    timestamp_column_name='lpep_pickup_datetime',
    problem_type='regression')

# Fit the calculator
calculator.fit(reference)
realized_results = calculator.calculate(analysis)

# Show comparison plot for realized and estimated performance
realized_results.compare(estimated_results).plot().show()

"""Different chunking methods
A chunk represents a single data point in the monitoring results. Recall that there are three methods for chunking your data: based on time, size, or the number of chunks.

In this exercise, you will chunk and visualize the results of the CBPE algorithm for the US Census dataset using size-based and number-based chunking methods.

The nannyml library is already imported."""

reference, analysis, analysis_gt = nannyml.load_us_census_ma_employment_data()

# Initialize the CBPE algorithm
cbpe = nannyml.CBPE(
    y_pred_proba='predicted_probability',
    y_pred='prediction',
    y_true='employed',
    metrics = ['roc_auc', 'accuracy', 'f1'],
    problem_type = 'classification_binary',
    chunk_number = 8,
)

cbpe = cbpe.fit(reference)
estimated_results = cbpe.estimate(analysis)
estimated_results.plot().show()

"""Modifying the thresholds
In the video, you observed how NannyML calculates threshold values and learned how to customize them to suit your solution.

In this exercise, your task is to define two custom standard deviation and custom thresholds and then apply them to the results obtained from the CBPE algorithm for the US Census dataset.

The reference and analysis sets have been pre-loaded as reference and analysis, along with the nannyml library."""

# Import custom thresholds
from nannyml.thresholds import StandardDeviationThreshold, ConstantThreshold

# Initialize custom thresholds
stdt = StandardDeviationThreshold(std_lower_multiplier=2, std_upper_multiplier=2)
ct = ConstantThreshold(lower=0.9, upper=0.98)

# Initialize the CBPE algorithm
estimator = nannyml.CBPE(
    problem_type='classification_binary',
    y_pred_proba='predicted_probability',
    y_pred='prediction',
    y_true='employed',
    metrics=['roc_auc', 'accuracy', 'f1'],
    thresholds={'f1': ct, 'accuracy' : stdt})

"""Interacting with results
In this exercise, you will filter, plot, and convert to the DataFrame the CBPE results obtained for the US Consensus dataset from the previous example. The display method here is used to show the plots and DataFrames that are called in the middle of the code.

The results from the CBPE estimator are preloaded in the estimated_results variable."""    

# Filter estimated results for the roc_auc metric and convert them to a dataframe
display(estimated_results.filter(metrics=['roc_auc']).to_df())

# Filter estimated results for the reference period and convert them to a dataframe
display(estimated_results.filter(period='reference').to_df())

# Filter the estimated results for the accuracy metric
display(estimated_results.filter(metrics=['accuracy']).plot().show())

# Filter the estimated results for the analysis period, as well as for accuracy and roc_auc metrics
display(estimated_results.filter(period='analysis', metrics=['accuracy', 'roc_auc']).plot().show())

"""Business calculation for hotel booking dataset
Previously, you were introduced to the challenge of predicting booking cancellations. Here, you will work with the actual Hotel Booking dataset, where a model predicts booking cancellations based on the customer's country of origin, time between booking and arrival, required parking spaces, and the chosen hotel.

The reference and analysis sets have already been loaded for you. Here are the first two rows:

  country  lead_time  parking_spaces       hotel  y_pred  y_pred_proba  is_canceled  timestamp
0  FRA     120        0               City Hotel  0       0.239983      0           2016-05-01
1  ITA     120        1               City Hotel  0       0.003965      0           2016-05-01
Your task is to check the model's monetary value and ROC AUC performance."""

# Custom business value thresholds
ct = ConstantThreshold(lower=0, upper=150000)
# Intialize the performance calculator
calc = PerformanceCalculator(problem_type='classification_binary',
			y_pred_proba='y_pred_proba',
  			timestamp_column_name="timestamp", 		
  			y_pred='y_pred',
  			y_true='is_canceled',
            chunk_period='m',
  			metrics=['business_value', 'roc_auc'],
  			business_value_matrix = [[0, -100],[-200, 1500]],
  			thresholds={"business_value": ct})
calc = calc.fit(reference)
calc_res = calc.calculate(analysis)
calc_res.filter(period='analysis').plot().show()

