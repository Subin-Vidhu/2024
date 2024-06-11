## Images for Reference

- Decision tree model

    ![alt text](image-1.png)

    ![alt text](image-2.png)

    ![alt text](image-3.png)

- Learning Process

    - How to choose what feature to split on at each node?

        - Greedy algorithm: At each node, choose the feature that maximizes the information gain.

        - Information gain: The reduction in entropy after a dataset is split on an attribute.

        - Entropy: The measure of randomness or uncertainty in a dataset.

        - Information gain = entropy(parent) - [weighted average]entropy(children)

        - Entropy = -Σp(x)log2p(x)

        - p(x) = fraction of examples in class x

    - When do you stop splitting?

        - When all data points belong to the same class.

        - When all data points belong to the same feature value.

        - When the tree reaches a maximum depth.

        - When the number of data points is less than a threshold.

- Measuring Purity

    - Entropy: The measure of randomness or uncertainty in a dataset, ie measure of impurity of a set of data points.

        ![alt text](image-4.png)

        ![alt text](image-5.png)

- Choosing a split: Information Gain

    - Information gain: The reduction in entropy after a dataset is split on an attribute.

        ![alt text](image-6.png)

        ![alt text](image-7.png)        

        ![alt text](image-6.png)

        ![alt text](image-7.png)