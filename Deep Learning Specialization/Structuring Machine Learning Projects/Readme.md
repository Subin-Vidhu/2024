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

**Structuring Machine Learning Projects**:

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