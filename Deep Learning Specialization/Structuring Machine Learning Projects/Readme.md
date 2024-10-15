# Notes


**Orthogonalization** refers to the process of identifying and tuning specific knobs or parameters to address different issues in the system's performance. The video also mentions the use of early stopping as a knob that affects multiple aspects simultaneously. The goal is to diagnose the bottleneck in the system's performance and identify the specific knobs to improve it.


To ensure that a supervised learning system performs well, there are four things that need to be addressed:

1. Performance on the training set: The system should perform well on the training set, meaning it should achieve acceptable results according to some predefined criteria. This criterion could vary depending on the application, but it generally involves achieving a certain level of accuracy or performance.

2. Performance on the development set: After performing well on the training set, the system should also perform well on a separate development set. The development set helps evaluate the system's generalization and ensures that it is not overfitting to the training data.

3. Performance on the test set: Once the system performs well on the development set, it should also perform well on a separate test set. The test set serves as an unbiased evaluation of the system's performance and helps assess its ability to generalize to unseen data.

4. Real-world performance: Finally, the system's performance on the test set should translate into real-world performance. This means that the system should deliver the desired outcome or result in the intended application or use case. It ensures that the system is not only performing well in an isolated evaluation but also in practical scenarios.


**Importance of Single Real Number Evaluation Metric in Machine Learning Projects**

Introduction:

The instructor emphasizes the importance of having a single real number evaluation metric in machine learning projects.
It allows teams to quickly compare and select the best classifiers or algorithms.

Evaluation Metrics:

- Precision and recall are commonly used evaluation metrics in machine learning.
- Precision measures the percentage of examples recognized as positive that are actually positive.
- Recall measures the percentage of actual positive examples that are correctly recognized.

Tradeoff between Precision and Recall:

- There is often a tradeoff between precision and recall.
- Teams need to consider both metrics when evaluating classifiers.


Introducing the F1 Score:

- The F1 score is a way to combine precision and recall into a single metric.
- It is defined as the harmonic mean of precision and recall.
- The F1 score provides a balanced evaluation of classifiers.

Examples of Using Evaluation Metrics:

- Example 1: Evaluating classifiers for a cat classifier.
Precision and recall can be used as evaluation metrics.
However, it is difficult to compare classifiers based on these two metrics alone.
The F1 score provides a single metric to quickly select the best classifier.

- Example 2: Evaluating classifiers in different geographies.
Tracking performance in each geography is important.
However, comparing multiple metrics for different geographies is challenging.
Computing the average performance provides a single metric for comparison.
Benefits of Single Evaluation Metric:

- Having a well- defined development set and a single evaluation metric speeds up the iterative process of improving machine learning algorithms.
- It allows teams to quickly compare and select the best classifiers or algorithms.

Conclusion:

- Using a single real number evaluation metric is crucial in machine learning projects.
- It improves efficiency and effectiveness in decision- making processes.
- The F1 score is a commonly used metric that combines precision and recall.
- Having a well- defined development set and a single evaluation metric accelerates the iterative process of improving machine learning algorithms.

**Satisficing and Optimizing Metrics**:

Introduction:

Combining multiple evaluation metrics can be challenging.
Satisficing metrics can be used alongside optimizing metrics.
Example 1: Classification Accuracy and Running Time:

Combining accuracy and running time into an overall evaluation metric.
Introducing the concept of satisficing metrics.
Choosing a classifier that maximizes accuracy while keeping running time below a certain threshold.
Example 2: Wake Word Detection System:

Maximizing accuracy of trigger word detection.
Limiting the number of false positives per day as a satisficing metric.
Guidelines for Setting up Training, Development, and Test Sets:
The need to evaluate metrics on different sets.
Introduction to training, development, and test sets.


**Train/Dev/Test Distribution**:

Introduction

The way you set up your training, development, and test sets can impact the progress of your machine learning team.
Setting up the development (dev) and test sets is crucial for evaluating different ideas and selecting the best model.
Setting up Dev and Test Sets

Dev Set:

Also known as the development set or hold out cross-validation set.
Used to evaluate different ideas and select the best model.
Innovate to improve dev set performance until you have a satisfactory result.
Test Set:

Used to evaluate the final model's performance.
Should come from the same distribution as the dev set.
Example:

Building a cat classifier for different regions (U.S, U.K, Europe, South America, India, China, Asia, Australia).
Bad idea: Dev set from four regions, test set from the other four regions (different distributions).
Recommended: Randomly shuffle data from all regions into both dev and test sets (same distribution).
Real-life Example:
A team optimized a model on loan approvals for medium-income zip codes.
Later, tested on low-income zip codes (different distribution).
Resulted in wasted time and effort.
Recommendations for Dev and Test Sets

Choose dev and test sets that reflect the data you expect to get in the future and consider important to perform well on.
Dev and test sets should come from the same distribution.
Put the target where you want to hit and have the team innovate efficiently to hit that target.
Conclusion

Setting up the dev set and evaluation metric defines the target you want to aim at.
Choosing the right training set will affect how well you can hit that target.
Revision Notes

The video explains the importance of setting up dev and test sets in machine learning projects.
It provides an example of setting up dev and test sets for a cat classifier in different regions.
The video highlights the problems that can arise when dev and test sets come from different distributions.
It recommends choosing dev and test sets that reflect future data and have the same distribution.
The video emphasizes the importance of setting the target correctly and efficiently innovating to hit that target.


**Size of the Dev and Test Sets**:

Introduction

The guidelines for setting up dev and test sets are changing in the Deep Learning era.
In earlier eras, a 70/30 or 60/20/20 split for train and test sets was reasonable.
With larger data sets in the modern era, it's reasonable to use a smaller percentage for dev and test sets.
Setting up Dev and Test Sets

For large data sets, consider using a smaller percentage for dev and test sets.
Example: If you have a million training examples, you can use 98% for training, 1% for dev, and 1% for test.
The purpose of the test set is to evaluate the overall performance of your system.
Set your test set to be big enough to give high confidence in the system's performance.
Train Dev Set vs. Test Set

Depending on your application, you may not need a high confidence measure of the overall performance.
If you only need data to train on and tune your system, a train dev set without a test set may be sufficient.
Having a separate test set is recommended to get an unbiased estimate of the system's performance.
Summary and Recommendations

In the era of big data, the old rule of thumb of a 70/30 split no longer applies.
Use more data for training and less for dev and test sets, especially with large data sets.
Set the dev set to be big enough for evaluation and idea comparison.
Set the test set to be big enough for evaluating the final system's performance.
Having a separate test set is reassuring, but a large dev set may suffice in some cases.
Changing Evaluation Metrics and Sets

Sometimes, during a machine learning problem, you may want to change the evaluation metric or dev and test sets.
This can be done partway through the problem to improve the system's performance.

**When to Change Dev/Test Sets and Metrics?**:

Introduction:

Placing a target for your team to aim at in a machine learning project.
Importance of evaluating and choosing the right evaluation metric.
Example of Evaluation Metric:

Building a cat classifier with classification error as the evaluation metric.
Algorithm A has 3% error, while Algorithm B has 5% error.
Algorithm A lets through pornographic images, making it unacceptable.
Algorithm B has higher error but does not have pornographic images.
Evaluation metric mispredicts the better algorithm in this case.
Changing the Evaluation Metric:

Need to change the evaluation metric or development set when it no longer correctly ranks algorithm preferences.
Introducing a weight term to give higher weight to pornographic images in the evaluation metric.
Modifying the cost function to incorporate the weights.
Evaluating on Real-World Data:

Evaluating classifiers on high-quality images may not correspond to real-world performance.
Need to consider the type of data the algorithm will encounter in the application.
Changing the evaluation metric or development/test set to better reflect real-world conditions.
Orthogonalization:

Breaking down the machine learning task into distinct steps.
Placing the target (defining the metric) and aiming at the target (optimizing the algorithm) as separate steps.
Importance of Evaluation Metric and Development Set:
Having an evaluation metric and development set allows for quicker decision-making and iteration.
Set up an initial evaluation metric and development set, even if not perfect, to drive team efficiency.
Can change the evaluation metric or development set later if needed.

**Why Human-Level Performance?**:


Introduction:
Comparing machine learning systems to human-level performance.
Reasons for the increased focus on human-level performance.

Progress Towards Human-Level Performance:
Progress tends to be rapid as you approach human-level performance.
After surpassing human-level performance, progress and accuracy slow down.
The performance approaches but never surpasses the Bayes optimal error.

Reasons for Slower Progress After Surpassing Human-Level Performance:
Human-level performance is often close to the Bayes optimal error.
Tools for improving performance are harder to apply once surpassing human-level performance.

Importance of Comparing to Human-Level Performance:
Humans are good at tasks like image recognition and language understanding.
Comparing to human-level performance helps understand bias and variance.

Module 2: ML Strategy

Introduction:
The importance of having a well-structured machine learning project.

Orthogonalization:
The concept of orthogonalization in machine learning projects.
Dividing the project into separate components to focus on specific tasks.

Setting Up Metrics:
Choosing the right evaluation metric for the project.
Metrics should align with the project's goals and objectives.

Comparing to Human-Level Performance:
The benefits of comparing machine learning systems to human-level performance.
Understanding the limitations and potential improvements.

Error Analysis:
Conducting manual error analysis to identify areas for improvement.
Analyzing bias and variance in the system.

Mismatched Training and Dev/Test Set:
Identifying and addressing issues related to mismatched training and dev/test sets.
Strategies for handling different data distributions.

Learning from Multiple Tasks:
Leveraging knowledge from multiple tasks to improve performance.
Transfer learning and multi-task learning approaches.

End-to-End Deep Learning:
The advantages and challenges of end-to-end deep learning.
When to use end-to-end deep learning and when to use traditional approaches.

**Avoidable Bias**:

Introduction:

Discusses the importance of knowing human level performance in machine learning algorithms.
Explains how the gap between algorithm performance and human performance indicates the fitting of the training set.

Bias and Variance:

Describes the tools to reduce bias or variance in machine learning algorithms.
Focuses on reducing bias when there is a large gap between algorithm performance and human performance.
Focuses on reducing variance when algorithm performance is close to human performance.

Human Level Error:

Considers human level error as a proxy for Bayes error or Bayes optimal error.
Explains that human level error is worse than Bayes error but not too far from it.
Shows how different human level errors affect the focus on bias or variance reduction tactics.

Avoidable Bias and Variance:

Introduces the concept of avoidable bias as the difference between Bayes error and training error.
Defines variance as the difference between training error and dev error.
Emphasizes that there is more potential for improvement in reducing variance than avoidable bias.

Decision Making:

Highlights the importance of understanding human level performance in decision making.
Explains how different scenarios require different tactics based on bias or variance avoidance.

Conclusion:
Mentions that there is more nuance in factoring human level performance into decision making.
Teases the next video, which goes deeper into understanding human level performance.

**Understanding Human-level Performance**:

Introduction to defining human-level performance: The video starts by discussing the concept of human-level performance in machine learning projects. It emphasizes the importance of defining human-level error as a benchmark for evaluating the performance of machine learning models.

Defining human-level error as a proxy for Bayes error: The video explains that human-level error can be used as an estimate for Bayes error, which represents the best possible error any function could achieve. It provides a medical image classification example to illustrate different levels of human performance and the need to define human-level error accurately.

Example of a medical image classification task: The video presents a scenario where a radiology image needs to be classified for diagnosis. It mentions that a typical untrained human achieves 3% error, while a typical radiologist achieves 1% error. An experienced doctor performs even better with 0.7% error, and a team of experienced doctors achieves a consensus opinion with 0.5% error.

Defining human-level error as 0.5%: The video discusses how to define human-level error based on the performance of a team of experienced doctors. It suggests using 0.5% as the estimate for Bayes error, as it represents the optimal error that cannot be higher than this value.

Understanding the relationship between human-level error, training error, and dev error: The video explains that the difference between human-level error and training error is a measure of avoidable bias, while the difference between training error and dev error indicates the variance problem in the learning algorithm.

Analyzing the measure of avoidable bias and variance: The video provides examples to demonstrate how the measure of avoidable bias and variance can help determine the focus of improvement. It discusses scenarios where bias reduction techniques, such as training a bigger network, are needed, and situations where variance reduction techniques, such as regularization or getting a bigger training set, should be prioritized.

Challenges in estimating bias and variance near human-level performance: The video highlights the difficulty in estimating bias and variance when the model's performance approaches human-level. It explains that as the performance gets closer to human-level, it becomes harder to determine the bias and variance effects accurately.

Importance of accurate estimation of Bayes error: The video emphasizes the significance of having an accurate estimate of Bayes error to make informed decisions about bias and variance reduction. It suggests that a better estimate of Bayes error can help identify the focus areas for improvement in machine learning projects.

Recap of the key points discussed in the video: The video concludes by summarizing the main takeaways, including the use of human-level error as a proxy for Bayes error, the relationship between human-level error, training error, and dev error, and the challenges in estimating bias and variance near human-level performance.