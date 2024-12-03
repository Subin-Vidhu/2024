from dlai_grader.grading import test_case, print_feedback
from types import FunctionType
from dlai_grader.io import suppress_stdout_stderr
import tensorflow as tf
import numpy as np


def parameter_count(model):
    total_params_solution, train_params_solution = 30_000, 30_000
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


def test_train_val_datasets(learner_func):
    def g():
        function_name = "train_val_datasets"

        cases = []
        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = "train_val_datasets has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        t = test_case()
        try:
            with suppress_stdout_stderr():
                train_dataset, val_dataset = learner_func()
        except Exception as e:
            t.failed = True
            t.msg = "There was an error evaluating train_val_datasets function"
            t.want = "No exceptions"
            t.got = f"{str(e)}"
            return [t]

        t = test_case()
        if not isinstance(train_dataset, tf.data.Dataset):
            t.failed = True
            t.msg = "Got a wrong type for output 'train_dataset'"
            t.want = tf.data.Dataset
            t.got = type(train_dataset)
            return [t]

        t = test_case()
        if not isinstance(val_dataset, tf.data.Dataset):
            t.failed = True
            t.msg = "Got a wrong type for output 'validation_dataset'"
            t.want = tf.data.Dataset
            t.got = type(val_dataset)
            return [t]

        text_tr, lab_tr = next(train_dataset.as_numpy_iterator())
        text_val, lab_val = next(val_dataset.as_numpy_iterator())

        # test batchsize
        t = test_case()
        if not text_tr.shape[0] == 32:
            t.failed = True
            t.msg = "Got a wrong batch size for train_dataset"
            t.want = 32
            t.got = text_tr.shape[0]
        cases.append(t)
        t = test_case()
        if not text_val.shape[0] == 32:
            t.failed = True
            t.msg = "Got a wrong batch size for train_dataset"
            t.want = 32
            t.got = text_val.shape[0]
        cases.append(t)

        # test element shapes
        t = test_case()
        if not text_tr.shape[1:] == (28, 28, 1):
            t.failed = True
            t.msg = "Got a wrong shape for images in for train_dataset"
            t.want = (28, 28, 1)
            t.got = text_tr.shape[1:]
        cases.append(t)

        t = test_case()
        if not text_val.shape[1:] == (28, 28, 1):
            t.failed = True
            t.msg = "Got a wrong shape for images in for validation_dataset"
            t.want = (28, 28, 1)
            t.got = text_val.shape[1:]
        cases.append(t)

        # Test that train and validation aren't swapped
        # Check the cardinality (i.e. number of batches) of each dataset
        t = test_case()
        if not train_dataset.cardinality() == 858:
            t.failed = True
            t.msg = "Got wrong cardinality (number of batches) for train_dataset"
            t.want = 858
            t.got = train_dataset.cardinality()
        cases.append(t)

        t = test_case()
        if not val_dataset.cardinality() == 225:
            t.failed = True
            t.msg = "Got wrong cardinality (number of batches) for validation_dataset"
            t.want = 225
            t.got = val_dataset.cardinality()
        cases.append(t)
        return cases

    cases = g()
    print_feedback(cases)


def test_create_model(learner_func):
    def g():
        function_name = "create_model"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = "create_model has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        t = test_case()
        try:
            model = learner_func()
        except Exception as e:
            t.failed = True
            t.msg = "There was an error evaluating create_model function"
            t.want = "No exceptions"
            t.got = f"{str(e)}"
            return [t]

        t = test_case()
        if not isinstance(model, tf.keras.models.Model):
            t.failed = True
            t.msg = "Got a wrong type for output create_model"
            t.want = tf.keras.models.Sequential
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

        # test input shape
        t = test_case()
        if not model.input_shape == (None, 28, 28, 1):
            t.failed = True
            t.msg = "Got wrong input shape for the model"
            t.want = (None, 28, 28, 1)
            t.got = model.input_shape
            return [t]

        t = test_case()

        if (model.loss == "sparse_categorical_crossentropy") | (
            isinstance(model.loss, tf.losses.SparseCategoricalCrossentropy)
        ):
            train_img = np.random.randint(0, 255, size=(1, 28, 28, 1))
            train_lab = np.random.randint(0, 24, size=(1,))
            train_dataset = tf.data.Dataset.from_tensor_slices(
                (train_img, train_lab)
            ).batch(1)
        elif (model.loss == "categorical_crossentropy") | (
            isinstance(model.loss, tf.losses.CategoricalCrossentropy)
        ):
            train_img = np.random.randint(0, 255, size=(1, 28, 28, 1))
            train_lab = np.random.randint(0, 24, size=(1, 24))
            train_dataset = tf.data.Dataset.from_tensor_slices(
                (train_img, train_lab)
            ).batch(1)
        else:
            t.failed = True
            t.msg = "Got a wrong loss"
            t.want = (
                "either 'categorical_crossentropy' or 'sparse_categorical_crossentropy'"
            )
            t.got = model.loss
            return [t]

        try:
            with suppress_stdout_stderr():
                hist = model.fit(train_dataset)
        except Exception as e:
            t.failed = True
            t.msg = "There was an error trying to fit the model"
            t.want = "No exceptions"
            t.got = f"str{e}"
            return [t]

        # test output shape
        t = test_case()
        if not model.output_shape == (None, 24):
            t.failed = True
            t.msg = "Got wrong output shape for the model"
            t.want = (None, 24)
            t.got = model.output_shape
        cases.append(t)

        # Test metrics
        t = test_case()
        if "accuracy" not in hist.history.keys():
            t.failed = True
            t.msg = "Got a wrong metric "
            t.want = "'accuracy' (there may be other metrics)"
            t.got = model.metrics_names[1:]
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
