from dlai_grader.grading import test_case, print_feedback
import tensorflow as tf
import numpy as np
from types import FunctionType


def parameter_count(model):
    total_params_solution, train_params_solution = 21_000_000, 21_000_000

    total_params = model.count_params()
    num_trainable_params = sum(
        [w.shape.num_elements() for w in model.trainable_weights]
    )

    total_msg = f"\033[92mYour model has {total_params:,} total parameters and the reference is {total_params_solution:,}"
    train_msg = f"\033[92mYour model has {num_trainable_params:,} trainable parameters and the reference is {train_params_solution:,}"

    if total_params > total_params_solution:
        total_msg += f"\n\033[91mWarning! this exceeds the reference which is {total_params_solution:,}. If the kernel crashes while training, switch to a simpler architecture."
    else:
        total_msg += "\033[92m. You are good to go!"

    if num_trainable_params > train_params_solution:
        train_msg += f"\n\033[91mWarning! this exceeds the reference which is {train_params_solution:,}. If the kernel crashes while training, switch to a simpler architecture."
    else:
        train_msg += "\033[92m. You are good to go!"

    print(total_msg)
    print()
    print(train_msg)


def test_train_data(data):
    def g():
        cases = []

        t = test_case()
        if not isinstance(data, tf.data.Dataset):
            t.failed = True
            t.msg = "train_data has incorrect type"
            t.want = tf.data.Dataset
            t.got = type(data)
            return [t]

        for images, labels in data.take(1):
            training_images = images
            training_labels = labels

        t = test_case()
        if not isinstance(training_images, tf.Tensor):
            t.failed = True
            t.msg = "images of train_data have incorrect type"
            t.want = tf.Tensor
            t.got = type(training_images)
            return [t]

        t = test_case()
        if not isinstance(training_labels, tf.Tensor):
            t.failed = True
            t.msg = "labels of train_data have incorrect type"
            t.want = tf.Tensor
            t.got = type(training_labels)
            return [t]

        training_images_dim = training_images.ndim

        t = test_case()
        if training_images_dim != 4:
            t.failed = True
            t.msg = "tensor of images has incorrect number of dimensions"
            t.want = 4
            t.got = training_images_dim
            return [t]

        dim_batch, *dims = training_images.shape
        dims = tuple(dims)

        t = test_case()
        if dim_batch != 10:
            t.failed = True
            t.msg = "incorrect number of elements in a batch"
            t.want = 10
            t.got = dim_batch
        cases.append(t)

        t = test_case()
        if dims != (150, 150, 3):
            t.failed = True
            t.msg = "incorrect shape for tensor of images"
            t.want = (150, 150, 3)
            t.got = dims
        cases.append(t)

        t = test_case()
        if np.max(training_images) != 1.0:
            t.failed = True
            t.msg = "incorrect maximum value of pixel in tensor"
            t.want = 1.0
            t.got = np.max(training_images)
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_create_and_compile_model(learner_func):
    def g():
        function_name = "create_and_compile_model"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        model = learner_func()

        t = test_case()
        if not isinstance(model, tf.keras.Model):
            t.failed = True
            t.msg = f"object returned by {function_name} has incorrect type"
            t.want = tf.keras.Model
            t.got = type(model)
            return [t]

        t = test_case()
        try:
            model_input = model.inputs[0]
        except Exception as e:
            t.failed = True
            t.msg = "your model is missing the Input"
            t.want = "a model with a defined Input"
            t.got = str(e)
            return [t]

        t = test_case()
        if not isinstance(model_input, tf.keras.KerasTensor):
            t.failed = True
            t.msg = "the input of your model has incorrect type"
            t.want = "a tf.keras.KerasTensor defined via tf.keras.Input"
            t.got = model_input
            return [t]

        input_shape = model.input_shape
        t = test_case()
        if input_shape != (None, 150, 150, 3):
            t.failed = True
            t.msg = "model has incorrect input_shape"
            t.want = (None, 150, 150, 3)
            t.got = input_shape
            return [t]

        test_images = np.zeros(shape=(10, 150, 150, 3))

        t = test_case()
        try:
            predictions = model.predict(test_images, verbose=False)
        except Exception as e:
            t.failed = True
            t.msg = "your model could not be used for inference on the train set"
            t.want = "no exceptions"
            t.got = str(e)
            return [t]

        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_training_history(hist):
    def g():
        cases = []

        t = test_case()
        if not isinstance(hist, tf.keras.callbacks.History):
            t.failed = True
            t.msg = "training_history has incorrect type"
            t.want = tf.keras.callbacks.History
            t.got = type(hist)
            return [t]

        if "accuracy" not in list(hist.history.keys()):
            t.failed = True
            t.msg = "training_history is missing 'accuracy' metric"
            t.want = "a metrics named 'accuracy'"
            t.got = list(hist.history.keys())
            return [t]

        hardcoded_epochs = hist.params["epochs"]
        trained_epochs = len(hist.epoch)

        t = test_case()
        if hardcoded_epochs != 15:
            t.failed = True
            t.msg = "incorrect number of epochs set for training"
            t.want = 15
            t.got = hardcoded_epochs
        cases.append(t)

        t = test_case()
        if trained_epochs == 15:
            t.failed = True
            t.msg = "the callback did not fire before reaching 15 epochs"
            t.want = "training for less than 15 epochs"
            t.got = f"model trained for {trained_epochs} epochs"
        cases.append(t)

        acc = hist.history["accuracy"][-1]

        t = test_case()
        if acc < 0.999:
            t.failed = True
            t.msg = "your model didn't achieve the required level of accuracy"
            t.want = "an accuracy of at least 0.999"
            t.got = f"{acc:.3f}"
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
