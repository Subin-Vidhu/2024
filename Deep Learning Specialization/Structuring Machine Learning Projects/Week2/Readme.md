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

- Deep learning algorithms require a large amount of training data, and teams often include any available data in the training set, even if it comes from a different distribution than the dev and test data.
- The video provides two examples to illustrate this concept:
    - Building a mobile app to recognize cat pictures: The team has 10,000 pictures from the mobile app and 200,000 professionally taken cat pictures from the web. They can either combine both datasets or use only the mobile app pictures for the dev and test sets.

    - Building a speech-activated rearview mirror: The team has 500,000 utterances from various speech recognition applications and a smaller dataset from the rearview mirror. They can either use all the data for training or split it between the training and dev/test sets.
- The video discusses the advantages and disadvantages of each approach:
- Option 1: Combining datasets for training, dev, and test sets:
    - Advantages: All sets come from the same distribution, making it easier to manage.

    - Disadvantages: The dev set may be dominated by data from a different distribution, leading to suboptimal performance on the desired distribution.

- Option 2: Using different datasets for training, dev, and test sets:
    - Advantages: The dev and test sets represent the desired distribution, allowing the team to optimize for it.

    - Disadvantages: The training distribution differs from the dev and test distributions, which can pose challenges.
- The video concludes that using different datasets for training, dev, and test sets can lead to better performance in the long term, despite the challenges it presents.
- The video also mentions that using all available data is not always the best approach and that there are cases where it is better to be selective.
- Definitions mentioned in the video:

    - Deep learning algorithms: Algorithms that use artificial neural networks with multiple layers to learn and make predictions.
    - Training data: Data used to train a machine learning model.
    - Dev and test data: Data used to evaluate the performance of a machine learning model.
    - Distribution: The pattern or spread of data points in a dataset.
    - Mobile app distribution: The distribution of images uploaded from a mobile app.
    - Web page distribution: The distribution of images downloaded from the web.
    - Utterances: Spoken words or phrases.
    - Speech recognition: The technology that converts spoken language into written text.

**Bias and Variance with Mismatched Data Distributions**

- Estimating the bias and variance of your learning algorithm helps prioritize what to work on next.
- Analyzing bias and variance changes when your training set comes from a different distribution than your dev and test sets.
- Error analysis involves looking at the training error and the error on the dev set.
- If the dev data comes from the same distribution as the training set, a large variance problem is identified.
- However, if the training and dev data come from different distributions, it is difficult to draw conclusions about variance.
- To tease out the effects of data mismatch and variance, a new subset of data called the training-dev set is defined.
- The training-dev set is a measure of variance, while the gap between the training-dev error and the dev error is a measure of data mismatch.
- Addressing data mismatch is challenging, but there are some things you can try to mitigate the problem.
- One approach is to randomly shuffle the training set and carve out a portion as the training-dev set.
- By comparing the error on the training set, training-dev set, and dev set, you can identify whether you have a variance or data mismatch problem.
- The general principles for error analysis involve looking at human level error, training set error, training-dev set error, and dev set error.
- The differences between these errors can help identify the presence of avoidable bias, variance, and data mismatch problems.

**Addressing Data Mismatch**

- Data Mismatch Problem:

    - When the training set comes from a different distribution than the dev and test set.
    - Error analysis helps identify the differences between the training set and the dev/test sets.

- Manual Error Analysis:

    - Analyzing the differences between the training set and the dev/test sets.
    Looking at the dev set to understand how it differs from the training set.
    - Example: Speech-activated rear-view mirror application, analyzing car noise and mis-recognition of street numbers.

- Making Training Data More Similar:

    - Find ways to make the training data more similar to the dev/test sets.
    - Simulate noisy in-car data to address car noise problems.
    - Collect more data of people speaking out numbers to improve street number recognition.

- Artificial Data Synthesis:

    - Technique to make the training data more similar to the dev/test sets.
    - Example: Synthesizing car noise by combining clean audio with recorded car noise.
    - Caution: Overfitting risk when synthesizing data from a small subset of the space.

- Learning from Multiple Types of Data:
    - Techniques to learn from multiple types of data simultaneously.

**Transfer Learning**

- Transfer learning is the idea of taking knowledge learned by a neural network from one task and applying it to a separate task.
- It involves training a neural network on an initial task, such as image recognition, and then adapting or transferring that knowledge to a different task, such as radiology diagnosis or wake word detection.
- In transfer learning, the last output layer of the neural network is removed, along with its weights, and a new set of randomly initialized weights is created for the last layer to output the desired predictions for the new task.
- The neural network is then retrained on a new dataset specific to the new task. Depending on the amount of data available, either only the last layer's weights or all the parameters in the network can be retrained.
- The initial phase of training on the initial task is called pre-training, and the subsequent training on the new task is called fine-tuning.
- Transfer learning is most useful when there is a lot of data available for the initial task and relatively less data for the new task.
- It makes sense when both tasks have the same input type and when low-level features learned from the initial task can be helpful for the new task.
- Transfer learning can significantly improve the performance of the new task, especially when there is limited data available for the new task.
- However, transfer learning may not be beneficial if there is already more data available for the new task compared to the initial task.

- Examples mentioned in the video:

    - Image Recognition and Radiology Diagnosis:

        - Training a neural network on a large image recognition dataset can help improve the performance of a radiology diagnosis system, even with limited radiology data.
        - The low-level features learned from image recognition, such as detecting edges and curves, can be useful for radiology diagnosis.

    - Speech Recognition and Wake Word Detection:

        - Training a neural network on a large speech recognition dataset can aid in building a wake word detection system, even with limited wake word data.
        - Knowledge about human speech learned from speech recognition can be applied to improve wake word detection.

**Multi-task Learning**

- Transfer learning is a sequential process where you learn from task A and then transfer that knowledge to task B.
- Multi-task learning is when you simultaneously train a neural network to perform multiple tasks at the same time.
- In multi-task learning, each task helps improve the performance of all the other tasks.
- An example of multi-task learning is building a self-driving car that needs to detect pedestrians, cars, stop signs, and traffic lights.
- In multi-task learning, the labels for each task are represented as a vector. For example, instead of having one label for a stop sign, you would have four labels: pedestrians, cars, stop signs, and traffic lights.
- To train a neural network for multi-task learning, you need to define the loss function, which is the average loss over the entire training set.
- Multi-task learning is beneficial when there is a large amount of data available for each task and when you can train a big enough neural network to perform well on all the tasks.
- Multi-task learning can provide a big boost in performance when there is a large amount of data available for all the tasks combined.
- Multi-task learning is more effective when the neural network is large enough to handle all the tasks simultaneously.
- If the neural network is not big enough, multi-task learning may not improve performance compared to training separate neural networks for each task.