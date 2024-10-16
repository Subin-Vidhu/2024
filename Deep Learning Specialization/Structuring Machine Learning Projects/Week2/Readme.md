## Error Analysis
**Carrying Out Error Analysis**

- Error analysis involves manually examining mistakes made by a learning algorithm to gain insights into improving its performance.

- An example is given of a cat classifier that misclassifies some dogs as cats.

- The video explains how to determine if it is worth focusing on the dog misclassification problem.

- The error analysis procedure involves getting a set of mislabeled examples and manually examining them.

- By counting the percentage of mislabeled examples that are dogs, the potential improvement in performance can be estimated.

- If a small percentage of errors are due to dogs, the improvement in performance by focusing on the dog problem may be limited.

- On the other hand, if a large percentage of errors are due to dogs, the potential improvement in performance can be significant.

- Error analysis can also be used to evaluate multiple ideas for improving performance, such as focusing on great cats or blurry images.

- By creating a table and counting the percentage of errors in each category, the most promising directions for improvement can be identified.

- Error analysis is a simple and effective way to prioritize and make better decisions in machine learning projects.

**Cleaning Up Incorrectly Labeled Data**

- Mislabeled examples refer to when the learning algorithm outputs the wrong value of Y.

- Incorrectly labeled examples refer to when the label assigned to a piece of data is actually incorrect.

- Deep learning algorithms are robust to random errors in the training set, as long as the errors are reasonably random.

- It may not be necessary to fix incorrectly labeled examples in the training set if the total dataset size is big enough and the percentage of errors is not too high.
- Deep learning algorithms are less robust to systematic errors, such as consistently labeling white dogs as cats.
- When considering incorrectly labeled examples in the dev set or test set, it is recommended to add an extra column to count the number of examples with incorrect labels.
- If the impact of incorrectly labeled examples on the dev set or test set is significant, it may be worth fixing the incorrect labels.
- Three numbers to consider when deciding whether to fix mislabeled examples are the overall dev set error, the percentage of errors due to incorrect labels, and the percentage of errors due to other causes.
- If a high fraction of mistakes on the dev set are due to incorrect labels, it is more worthwhile to fix them.
- When manually examining and fixing labels, it is recommended to apply the same process to both the dev set and test set.
- It is also important to examine examples that the algorithm got right, not just the ones it got wrong.
- Fixing labels in the training set may not be as important as fixing labels in the dev and test sets.
- Manual error analysis and human insight are important in building practical machine learning systems.
- It is recommended to spend time manually looking at examples and counting errors to prioritize next steps in a machine learning project.

**Build your First System Quickly, then Iterate**

- It mentions that there are many directions to improve a machine learning application, such as making it more robust to noisy background, accented speech, far-field speech recognition, and handling speech from young children.
- The video recommends setting up a dev/test set and metric as a target for the initial system.
- It suggests building an initial machine learning system quickly and evaluating its performance against the dev/test set and metric.
- Bias/variance analysis and error analysis are mentioned as tools to prioritize the next steps in improving the system.
- The video emphasizes the value of having a trained system to localize bias/variance and identify areas for improvement.
- It advises not to overthink or make the first system too complicated, especially when tackling a new problem for the first time.
- The video highlights the common tendency to overthink and build something too complicated, and suggests using a quick and dirty implementation to guide further improvements.
- It mentions that the advice applies less strongly if the application area has prior experience or a significant body of academic literature to draw upon.
- The video concludes by encouraging the viewer to build something quick and dirty, use analysis to prioritize improvements, and focus on building a system that works well.

## Mismatched Training and Dev/Test Set

**Training and Testing on Different Distributions**

