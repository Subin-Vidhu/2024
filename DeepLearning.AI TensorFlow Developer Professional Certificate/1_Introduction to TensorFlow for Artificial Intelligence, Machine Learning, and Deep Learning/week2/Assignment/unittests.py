import os
from dlai_grader.grading import test_case, print_feedback
from dlai_grader.io import suppress_stdout_stderr
import tensorflow as tf
from types import FunctionType


data_path = os.path.join(os.getcwd(), "data/mnist.npz")

(x_train, y_train), _ = tf.keras.datasets.mnist.load_data(path=data_path)
x_train = x_train / 255.0


def parameter_count(model):
    total_params_solution, train_params_solution = 410_000, 410_000

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
        if input_shape != (None, 28, 28):
            t.failed = True
            t.msg = "model has incorrect input_shape"
            t.want = (None, 28, 28)
            t.got = input_shape
            return [t]

        t = test_case()
        try:
            predictions = model.predict(x_train[:7], verbose=False)
        except Exception as e:
            t.failed = True
            t.msg = "your model could not be used for inference on the train set"
            t.want = "no exceptions"
            t.got = str(e)
            return [t]

        cases.append(t)

        t = test_case()
        if predictions.shape != (7, 10):
            t.failed = True
            t.msg = "incorrect shape for the predictions of the first 7 items in the train set"
            t.want = (7, 10)
            t.got = predictions.shape
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_EarlyStoppingCallback(learner_class):
    def g():
        class_name = "EarlyStoppingCallback"

        cases = []

        t = test_case()
        if not isinstance(learner_class, type):
            t.failed = True
            t.msg = f"{class_name} has incorrect type"
            t.want = "a class called {class_name}"
            t.got = type(learner_class)
            return [t]

        t = test_case()
        if not issubclass(learner_class, tf.keras.callbacks.Callback):
            t.failed = True
            t.msg = "EarlyStoppingCallback didn't inherit from the correct class"
            t.want = tf.keras.callbacks.Callback
            t.got = learner_class.__base__
            return [t]

        class DummyModel(tf.keras.Model):
            def __init__(self):
                self.stop_training = False

        test_cases = [
            (False, {"logs": {"accuracy": 0.5}}),
            (False, {"logs": {"accuracy": 0.97}}),
            (False, {"logs": {"accuracy": 0.979}}),
            (True, {"logs": {"accuracy": 0.98}}),
            (True, {"logs": {"accuracy": 0.981}}),
            (True, {"logs": {"accuracy": 0.99}}),
        ]

        with suppress_stdout_stderr():
            for stop, t_case in test_cases:
                t = test_case()
                model = DummyModel()
                callback = learner_class()
                callback.set_model(model)
                callback.on_epoch_end(10, logs=t_case["logs"])
                msg = "continued" if stop else "stopped"
                if callback.model.stop_training != stop:
                    t.failed = True
                    t.msg = "Callback didn't fire when expected"
                    t.want = "Callback should fire only when accuracy >= 0.98"
                    t.got = (
                        f"Training {msg} when accuracy = {t_case['logs']['accuracy']}"
                    )
                cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_training_history(learner_hist):
    def g():
        cases = []

        hist = learner_hist

        t = test_case()
        if not isinstance(hist, tf.keras.callbacks.History):
            t.failed = True
            t.msg = "training_history has incorrect type"
            t.want = tf.keras.callbacks.History
            t.got = type(hist)
            return [t]

        hardcoded_epochs = hist.params["epochs"]
        trained_epochs = len(hist.epoch)

        t = test_case()
        if hardcoded_epochs != 10:
            t.failed = True
            t.msg = "incorrect number of epochs set for training"
            t.want = 10
            t.got = hardcoded_epochs
        cases.append(t)

        t = test_case()
        if trained_epochs == 10:
            t.failed = True
            t.msg = "the callback did not fire before reaching 10 epochs"
            t.want = "training for less than 10 epochs"
            t.got = f"model trained for {trained_epochs} epochs"
        cases.append(t)

        acc = hist.history["accuracy"][-1]

        t = test_case()
        if acc < 0.98:
            t.failed = True
            t.msg = "your model didn't achieve the required level of accuracy"
            t.want = "an accuracy of at least 0.98"
            t.got = f"{acc:.3f}"
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
