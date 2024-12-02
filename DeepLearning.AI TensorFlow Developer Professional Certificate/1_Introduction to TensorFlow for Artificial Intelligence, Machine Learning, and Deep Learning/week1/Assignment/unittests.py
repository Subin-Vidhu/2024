from dlai_grader.grading import test_case, print_feedback
import tensorflow as tf
import numpy as np
import math
from types import FunctionType


def test_define_and_compile_model(learner_func):
    def g():
        function_name = "define_and_compile_model"

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
        if input_shape != (None, 1):
            t.failed = True
            t.msg = "model has incorrect input_shape"
            t.want = (None, 1)
            t.got = input_shape
            return [t]

        layers = model.layers

        t = test_case()
        if len(layers) != 1:
            t.failed = True
            t.msg = "model has incorrect number of layers"
            t.want = 1
            t.got = len(layers)
        cases.append(t)

        dense = layers[0]

        t = test_case()
        if not isinstance(dense, tf.keras.layers.Dense):
            t.failed = True
            t.msg = "first layer has incorrect type"
            t.want = tf.keras.layers.Dense
            t.got = type(dense)
        cases.append(t)

        t = test_case()
        if dense.units != 1:
            t.failed = True
            t.msg = "incorrect number of units for Dense layer"
            t.want = 1
            t.got = dense.units
        cases.append(t)

        t = test_case()
        if not isinstance(model.optimizer, tf.keras.optimizers.SGD):
            t.failed = True
            t.msg = "incorrect optimizer used for model"
            t.want = tf.keras.optimizers.SGD
            t.got = type(model.optimizer)
        cases.append(t)

        t = test_case()
        if isinstance(model.loss, tf.keras.losses.Loss):
            if not isinstance(model.loss, tf.keras.losses.MeanSquaredError):
                t.failed = True
                t.msg = "incorrect loss function used for model"
                t.want = tf.keras.losses.MeanSquaredError
                t.got = model.loss

        elif isinstance(model.loss, str):
            if model.loss not in ["mean_squared_error", "mse"]:
                t.failed = True
                t.msg = "incorrect loss function used for model"
                t.want = "'mean_squared_error' or 'mse'"
                t.got = model.loss
        else:
            t.failed = True
            t.msg = "loss function should be a string or a class from tf.keras.losses"
            t.want = "a string or a class from tf.keras.losses"
            t.got = type(model.loss)
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_create_training_data(learner_func):
    def g():
        function_name = "create_training_data"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        data = learner_func()

        t = test_case()
        if not isinstance(data, tuple):
            t.failed = True
            t.msg = f"object returned by {function_name} has incorrect type"
            t.want = tuple
            t.got = type(data)
            return [t]

        n_bedrooms, price_in_hundreds_of_thousands = data

        t = test_case()
        if not isinstance(n_bedrooms, np.ndarray):
            t.failed = True
            t.msg = "n_bedrooms has incorrect type"
            t.want = np.ndarray
            t.got = type(n_bedrooms)
            return [t]

        t = test_case()
        if not isinstance(price_in_hundreds_of_thousands, np.ndarray):
            t.failed = True
            t.msg = "price_in_hundreds_of_thousands has incorrect type"
            t.want = np.ndarray
            t.got = type(price_in_hundreds_of_thousands)
            return [t]

        t = test_case()
        if "float" not in n_bedrooms.dtype.name:
            t.failed = True
            t.msg = "incorrect dtype for n_bedrooms tensor"
            t.want = "float"
            t.got = n_bedrooms.dtype.name
        cases.append(t)

        t = test_case()
        if "float" not in price_in_hundreds_of_thousands.dtype.name:
            t.failed = True
            t.msg = "incorrect dtype for price_in_hundreds_of_thousands tensor"
            t.want = "float"
            t.got = price_in_hundreds_of_thousands.dtype.name
        cases.append(t)

        t = test_case()
        if n_bedrooms.shape != (6,):
            t.failed = True
            t.msg = "incorrect shape for n_bedrooms tensor"
            t.want = (6,)
            t.got = n_bedrooms.shape
        cases.append(t)

        t = test_case()
        if price_in_hundreds_of_thousands.shape != (6,):
            t.failed = True
            t.msg = "incorrect shape for price_in_hundreds_of_thousands tensor"
            t.want = (6,)
            t.got = price_in_hundreds_of_thousands.shape
        cases.append(t)

        loaded_data = np.load("data/saved_arrays.npz")
        features = loaded_data["features"]
        targets = loaded_data["targets"]

        t = test_case()
        if not np.allclose(n_bedrooms, features):
            t.failed = True
            t.msg = "incorrect values for n_bedrooms tensor"
            t.want = "a numpy array with values of the number of bedrooms for houses with 1 up to 6 bedrooms"
            t.got = n_bedrooms
        cases.append(t)

        t = test_case()
        if not np.allclose(price_in_hundreds_of_thousands, targets):
            t.failed = True
            t.msg = "incorrect values for price_in_hundreds_of_thousands tensor"
            t.want = "a numpy array with values of the prices for houses with 1 up to 6 bedrooms"
            t.got = price_in_hundreds_of_thousands
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_trained_model(model):
    def g():
        cases = []

        t = test_case()
        if not isinstance(model, tf.keras.Model):
            t.failed = True
            t.msg = "trained_model has incorrect type"
            t.want = tf.keras.Model
            t.got = type(model)
            return [t]

        new_n_bedrooms = np.array([7.0])
        predicted_price = model.predict([new_n_bedrooms], verbose=False).item()
        new_n_bedrooms = new_n_bedrooms.item()
        expected_price = 0.5 + (0.5 * new_n_bedrooms)
        t = test_case()
        close = math.isclose(predicted_price, expected_price, abs_tol=0.25)
        if not close:
            t.failed = True
            t.msg = f"prediction is not close enough to {expected_price} for houses with {new_n_bedrooms} bedrooms"
            t.want = (
                f"a value close to {expected_price} (with absolute tolerance of 0.25)"
            )
            t.got = f"{predicted_price:.2f}"

        cases.append(t)

        new_n_bedrooms = np.array([10.0])
        predicted_price = model.predict([new_n_bedrooms], verbose=False).item()
        new_n_bedrooms = new_n_bedrooms.item()
        expected_price = 0.5 + (0.5 * new_n_bedrooms)
        t = test_case()
        close = math.isclose(predicted_price, expected_price, abs_tol=0.25)
        if not close:
            t.failed = True
            t.msg = f"prediction is not close enough to {expected_price} for houses with {new_n_bedrooms} bedrooms"
            t.want = (
                f"a value close to {expected_price} (with absolute tolerance of 0.25)"
            )
            t.got = f"{predicted_price:.2f}"

        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
