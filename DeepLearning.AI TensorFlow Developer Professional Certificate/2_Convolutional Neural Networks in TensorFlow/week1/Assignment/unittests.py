import numpy as np
from dlai_grader.grading import test_case, print_feedback
from types import FunctionType
import tensorflow as tf
from dlai_grader.io import suppress_stdout_stderr


def parameter_count(model):
    total_params_solution, train_params_solution = 10_000_000, 10_000_000
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
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        try:
            with suppress_stdout_stderr():
                train_dataset, validation_dataset = learner_func()
        except Exception as e:
            t.failed = True
            t.msg = f"There was an error evaluating the {function_name} function."
            t.want = "No exceptions"
            t.got = f"{str(e)}"
            return [t]

        t = test_case()
        if not isinstance(train_dataset, tf.data.Dataset):
            t.failed = True
            t.msg = "There was an error with the output type of train_dataset."
            t.want = tf.data.Dataset
            t.got = type(train_dataset)
            return [t]

        t = test_case()
        if not isinstance(validation_dataset, tf.data.Dataset):
            t.failed = True
            t.msg = "There was an error with the output type of validation_dataset."
            t.want = tf.data.Dataset
            t.got = type(validation_dataset)
            return [t]

        for images, _ in train_dataset.take(1):
            training_images = images

        t = test_case()
        if not isinstance(training_images, tf.Tensor):
            t.failed = True
            t.msg = "images of training_dataset have incorrect type"
            t.want = tf.Tensor
            t.got = type(training_images)
            return [t]

        training_images_dim = training_images.ndim

        t = test_case()
        if training_images_dim != 4:
            t.failed = True
            t.msg = "tensor of training images has incorrect number of dimensions"
            t.want = 4
            t.got = training_images_dim
            return [t]

        for images, _ in validation_dataset.take(1):
            validation_images = images

        t = test_case()
        if not isinstance(validation_images, tf.Tensor):
            t.failed = True
            t.msg = "images of validation_dataset have incorrect type"
            t.want = tf.Tensor
            t.got = type(validation_images)
            return [t]

        validation_images_dim = validation_images.ndim

        t = test_case()
        if validation_images_dim != 4:
            t.failed = True
            t.msg = "tensor of validation images has incorrect number of dimensions"
            t.want = 4
            t.got = validation_images_dim
            return [t]

        args = [
            ("training", train_dataset._common_args, train_dataset.file_paths[0]),
            (
                "validation",
                validation_dataset._common_args,
                validation_dataset.file_paths[0],
            ),
        ]

        for dataset, ds, fp in args:
            output_shape_x = ds["output_shapes"][0]
            output_shape_y = ds["output_shapes"][1]
            t = test_case()
            if not output_shape_x == [None, 150, 150, 3]:
                t.failed = True
                t.msg = f"Incorrect image size in {dataset} dataset"
                t.want = "Shape of an output image batch must be (None, 150, 150, 3). Perhaps you passed an incorrect argument to image_size"
                t.got = f"{output_shape_x}"
            cases.append(t)

            t = test_case()
            if not output_shape_y == [None, 1]:
                t.failed = True
                t.msg = f"Incorrect label size in {dataset} dataset"
                t.want = "Shape of an output label batch must be (None, 1). Perhaps you passed an incorrect argument for label_mode"
                t.got = f"{output_shape_y}"
            cases.append(t)

        # Test number of train classes
        t = test_case()
        if not len(train_dataset.class_names) == 2:
            t.failed = True
            t.msg = "Wrong number of training classes"
            t.want = 2
            t.got = len(train_dataset.class_names)
        cases.append(t)

        # Test number of validation classes
        t = test_case()
        if not len(validation_dataset.class_names) == 2:
            t.failed = True
            t.msg = "Wrong number of validation classes"
            t.want = 2
            t.got = len(validation_dataset.class_names)
        cases.append(t)

        n_train_files = len(train_dataset.file_paths)
        n_validation_files = len(validation_dataset.file_paths)
        total_files = n_train_files + n_validation_files

        t = test_case()
        if total_files != 22434:
            t.failed = True
            t.msg = "Incorrect number of files. Check the directory you specified"
            t.want = 22434
            t.got = total_files
        cases.append(t)

        t = test_case()
        if n_train_files != 20191:
            t.failed = True
            t.msg = "Incorrect number of files used for training. Check the validation_split or the directory"
            t.want = 20191
            t.got = n_train_files
        cases.append(t)

        t = test_case()
        if n_validation_files != 2243:
            t.failed = True
            t.msg = "Incorrect number of files used for validation. Check the validation_split or the directory"
            t.want = 2243
            t.got = n_validation_files
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
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        t = test_case()

        try:
            model = learner_func()
        except Exception as e:
            t.failed = True
            t.msg = f"There was an error evaluating the {function_name} function."
            t.want = "No exceptions"
            t.got = f"{str(e)}"
            return [t]

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

        layers = model.layers

        t = test_case()
        if not isinstance(layers[0], tf.keras.layers.Rescaling):
            t.failed = True
            t.msg = "First layer is not a Rescaling layer. Aborting test. This function as it is will fail when grading."
            t.want = f"A layer of type {type(tf.keras.layers.Rescaling(1))}, from tf.keras.layers.Rescaling"
            t.got = type(layers[0])
            return [t]

        elif not np.isclose(layers[0].scale, 0.00392156862745098):
            t.failed = True
            t.msg = "Rescaling layer has not the correct scaling parameter."
            t.want = "1./255 or 0.00392156862745098"
            t.got = f"{layers[0].scale}"

        cases.append(t)

        convolution_layers = [
            layer for layer in layers if isinstance(layer, tf.keras.layers.Conv2D)
        ]

        t = test_case()

        if len(convolution_layers) < 3:
            t.failed = True
            t.msg = "There are fewer than 3 2D convolution layers."
            t.want = "At least 3 layers of the form tf.keras.layers.Conv2D."
            t.got = f"Got {len(convolution_layers)} layers of the form tf.keras.layers.Conv2D"

        cases.append(t)

        last_layer = layers[-1]

        t = test_case()
        if not isinstance(last_layer, tf.keras.layers.Dense):
            t.failed = True
            t.msg = "Last layer must be a Dense layer. Probably fitting the model will fail."
            t.want = "Last layer as a tf.keras.layers.Dense object"
            t.got = f"{type(last_layer)}"
            return [t]

        t = test_case()
        if last_layer.units > 2:
            t.failed = True
            t.msg = "Number of units for the last Dense layer is incorrect."
            t.want = "1 or 2 units"
            t.got = last_layer.units
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
            (False, {"logs": {"accuracy": 0.5, "val_accuracy": 0.5}}),
            (False, {"logs": {"accuracy": 0.5, "val_accuracy": 0.99}}),
            (False, {"logs": {"accuracy": 0.99, "val_accuracy": 0.5}}),
            (False, {"logs": {"accuracy": 0.94, "val_accuracy": 0.79}}),
            (False, {"logs": {"accuracy": 0.95, "val_accuracy": 0.79}}),
            (False, {"logs": {"accuracy": 0.94, "val_accuracy": 0.8}}),
            (True, {"logs": {"accuracy": 0.95, "val_accuracy": 0.8}}),
            (True, {"logs": {"accuracy": 0.951, "val_accuracy": 0.81}}),
            (True, {"logs": {"accuracy": 0.99, "val_accuracy": 0.99}}),
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
                    t.want = "Callback should fire only when accuracy >= 0.95 and validation accuracy >= 0.8"
                    t.got = f"Training {msg} when accuracy = {t_case['logs']['accuracy']} and validation accuracy = {t_case['logs']['val_accuracy']}"
                cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
