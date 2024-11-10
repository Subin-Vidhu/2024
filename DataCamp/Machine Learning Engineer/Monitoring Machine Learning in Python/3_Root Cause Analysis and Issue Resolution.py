"""Drift in hotel booking dataset
In the previous chapter, you calculated the business value and ROC AUC performance for a model that predicts booking cancellations. You noticed a few alerts in the resulting plots, which is why you need to investigate the presence of drift in the analysis data.

In this exercise, you will initialize the multivariate drift detection method and compare its results with the performance results calculated in the previous chapter.

StandardDeviationThreshold is already imported along with business value, and ROC AUC results stored in the perf_results variable and feature_column_names are already defined."""

# Create standard deviation thresholds
stdt = StandardDeviationThreshold(std_lower_multiplier=2, std_upper_multiplier=1)

# Define feature columns
feature_column_names = ["country", "lead_time", "parking_spaces", "hotel"]

# Intialize, fit, and show results of multivariate drift calculator
mv_calc = nannyml.DataReconstructionDriftCalculator(
    column_names=feature_column_names,
	threshold = stdt,
    timestamp_column_name='timestamp',
    chunk_period='m')
mv_calc.fit(reference)
mv_results = mv_calc.calculate(analysis)
mv_results.filter(period='analysis').compare(perf_results).plot().show()

"""Univariate drift detection for hotel booking dataset
In the previous exercises, we established using the multivariate drift detection method that the shift in data in January is responsible for the alert in the ROC AUC metric and the negative business value of the model.

In this exercise, you will use a univariate drift detection method to find the feature and explanation behind the drift.

The reference and analysis sets are already pre-loaded for you."""

# Intialize the univariate drift calculator
uv_calc = nannyml.UnivariateDriftCalculator(
    column_names=feature_column_names,
    timestamp_column_name='timestamp',
    chunk_period='m',
    continuous_methods=['wasserstein', 'jensen_shannon'],
    categorical_methods=['l_infinity', 'chi2'],
)

# Plot the results
uv_calc.fit(reference)
uv_results = uv_calc.calculate(analysis)
uv_results.plot().show()

"""Ranking the univariate results
In the previous exercises, you ended up with eight plots. In this exercise your task is to rank them based on the number of the alerts and the correlation with the ROC AUC performance.

The univariate results are pre-loaded and stored in uv_results variable, and performance results are stored in perf_results variable."""

# Initialize the alert count ranker
alert_count_ranker = nannyml.AlertCountRanker()
alert_count_ranked_features = alert_count_ranker.rank(
    uv_results.filter(methods=['wasserstein', 'l_infinity']))

display(alert_count_ranked_features)

# Initialize the correlation ranker
correlation_ranker = nannyml.CorrelationRanker()
correlation_ranker.fit(perf_results.filter(period='reference'))

correlation_ranked_features = correlation_ranker.rank(
    uv_results.filter(methods=['wasserstein', 'l_infinity']),
    perf_results)
display(correlation_ranked_features)

"""Visualizing drifting features
After ranking the univariate results, you know that drift hotel and country features are impacting the model's performance the most. In this exercise, you will look at the drift results and distribution plots of them to determine the root cause of the problem.

The results from the univariate drift calculator are stored in the uv_results variable."""

# Filter and create drift plots
drift_results = uv_results.filter(
    period='analysis',
    column_names=['hotel', 'country']
    ).plot(kind='drift')

# Filter and create distribution plots
distribution_results = uv_results.filter(
    period='analysis',
    column_names=['hotel', 'country']
    ).plot(kind='distribution')

# Show the plots
drift_results.show()
distribution_results.show()

"""Data quality checks
As you learned in the previous video, missing values can result in a loss of valuable information and potentially lead to incorrect interpretations. Similarly, the presence of unseen values can also affect your model's confidence.

In this exercise, your goal is to explore whether the hotel booking dataset contains missing values and identify any unseen values. The reference and analysis datasets are already loaded, along with the nannyml library.

A quick reminder, if you can't recall the column types, you can easily explore the data using the .head() method."""

# Define analyzed categorical columns
categorical_columns = ['country', 'hotel']

# Intialize unseen values calculator
us_calc = nannyml.UnseenValuesCalculator(
  	column_names=categorical_columns, 
  	chunk_period='m', 
  	timestamp_column_name='timestamp'
)

# Fit, calculate and plot the results
us_calc.fit(reference)
us_results = us_calc.calculate(analysis)
us_results.filter(period='analysis').plot().show()

"""Summary statistics
Recall from the previous lesson that NannyML provides five methods for tracking statistical changes in your features.

In this exercise, you will focus on examining the lead_time feature from the Hotel Booking dataset, which indicates how many days in advance a booking was made. By using summation, median, and standard deviation statistics, you can gain valuable insights into how customer booking behavior has evolved over time.

It's important to note that both the reference and analysis sets, as well as the nannyml library, are already pre-loaded and ready for use."""

# Define analyzed column
analyzed_column = ['lead_time']

# Intialize standard deviation values calculator
std_calc = nannyml.SummaryStatsStdCalculator(
    column_names=analyzed_column, 
    chunk_period='m', 
    timestamp_column_name='timestamp'
)

# Fit, calculate and plot the results
std_calc.fit(reference)
std_calc_res = std_calc.calculate(analysis)
std_calc_res.filter(period="analysis").plot().show()

"""Implementing a monitoring workflow
Throughout the course, you've learned about the monitoring workflow. The first step is performance monitoring. If there are negative changes, the next steps involve multivariate drift detection to identify if drift caused the performance drop, followed by univariate drift detection to pinpoint the cause in individual features. Once the investigation results are in, you can take steps to resolve the issue.

To solidify this knowledge, in the exercise, you'll apply this process to the US Consensus dataset. The reference and analysis datasets are pre-loaded, and you have access to the CBPE estimator, uv_calc univariate calculator, and an alert_count_ranker for feature drift ranking."""

# Estimate the performance
estimator.fit(reference)
estimated_results = estimator.estimate(analysis)

# Calculate multivariate drift
mv_calc = nannyml.DataReconstructionDriftCalculator(column_names=features, chunk_size=5000)
mv_calc.fit(reference)
mv_results = mv_calc.calculate(analysis)
display(mv_results.filter(period="analysis").compare(estimated_results).plot().show())

estimator.fit(reference)
estimated_performance = estimator.estimate(analysis)
mv_calc = nannyml.DataReconstructionDriftCalculator(column_names=features, chunk_size=5000)
mv_calc.fit(reference)
mv_results = mv_calc.calculate(analysis)

# Calculate univariate drift
uv_calculator.fit(reference)
uv_results = uv_calculator.calculate(analysis)

# Check the most drifting features
alert_count_ranked_features = alert_count_ranker.rank(uv_results)
display(alert_count_ranked_features.head())