from dlai_grader.grading import test_case, print_feedback
import tensorflow as tf
from types import FunctionType
from dlai_grader.io import suppress_stdout_stderr


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
            t.expected = "No exceptions"
            t.got = f"{str(e)}"
            return [t]

        t = test_case()
        if not isinstance(train_dataset, tf.data.Dataset):
            t.failed = True
            t.msg = "There was an error with the output type of train_dataset."
            t.expected = tf.data.Dataset
            t.got = type(train_dataset)
            return [t]

        t = test_case()
        if not isinstance(validation_dataset, tf.data.Dataset):
            t.failed = True
            t.msg = "There was an error with the output type of validation_dataset."
            t.expected = tf.data.Dataset
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

        t = test_case()
        target_size = train_dataset.as_numpy_iterator().next()[0].shape
        # Test train_dataset input shape
        t = test_case()
        img_size = target_size[1:3]
        if not img_size == (150, 150):
            t.failed = True
            t.msg = "incorrect value for image_size for training_dataset"
            t.want = (150, 150)
            t.got = img_size
        cases.append(t)

        # Test train batch size
        batch_size_tr = target_size[0]
        t = test_case()
        if not batch_size_tr == 32:
            t.failed = True
            t.msg = "training batch_size has incorrect value"
            t.want = 32
            t.got = batch_size_tr
        cases.append(t)

        target_size = validation_dataset.as_numpy_iterator().next()[0].shape
        # Test validation_dataset input shape
        t = test_case()
        img_size = target_size[1:3]
        if not img_size == (150, 150):
            t.failed = True
            t.msg = "incorrect value for image_size for validation_dataset"
            t.want = (150, 150)
            t.got = img_size
        cases.append(t)

        # Test validation_dataset batch size
        batch_size_val = target_size[0]
        t = test_case()
        if not batch_size_val == 32:
            t.failed = True
            t.msg = "validation batch_size has incorrect value"
            t.want = 32
            t.got = batch_size_val
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

        t = test_case()
        if n_train_files != 1027:
            t.failed = True
            t.msg = "Incorrect number of files used for training. Check your training directory"
            t.want = 1027
            t.got = n_train_files
        cases.append(t)

        n_validation_files = len(validation_dataset.file_paths)
        t = test_case()
        if n_validation_files != 256:
            t.failed = True
            t.msg = "Incorrect number of files used for validation. Check your validation directory"
            t.want = 256
            t.got = n_validation_files
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_create_pre_trained_model(learner_func):
    def g():
        function_name = "create_pre_trained_model"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = "learner_func has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        t = test_case()
        try:
            pretrained_model = learner_func()
        except Exception as e:
            t.failed = True
            t.msg = f"There was an error evaluating {function_name} function"
            t.want = "No exceptions"
            t.got = f"{e}"
            return [t]

        t = test_case()
        if not isinstance(pretrained_model, tf.keras.Model):
            t.failed = True
            t.msg = "Got wrong output type for create_pre_trained_model function"
            t.want = tf.keras.Model
            t.got = type(pretrained_model)
            return [t]

        # test input shape
        input_shape = pretrained_model.input_shape
        t = test_case()
        if not input_shape == (None, 150, 150, 3):
            t.failed = True
            t.msg = "Incorrect input_shape for InceptionV3 model"
            t.want = (None, 150, 150, 3)
            t.got = input_shape
        cases.append(t)

        # Test number of parameters
        t = test_case()
        if not pretrained_model.count_params() == 21802784:
            t.failed = True
            t.msg = "Got wrong number of parameters for pre_trained_model"
            t.want = 21802784
            t.got = pretrained_model.count_params()
        cases.append(t)

        # test number of trainable parameters
        t = test_case()
        num_trainable_params = sum(
            [w.shape.num_elements() for w in pretrained_model.trainable_weights]
        )
        if not num_trainable_params == 0:
            t.failed = True
            t.msg = "Incorrect number of trainable parameters for InceptionV3 model"
            t.want = 0
            t.got = num_trainable_params
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_output_of_last_layer(learner_func, pretrained_model):
    def g():
        function_name = "output_of_last_layer"

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
            with suppress_stdout_stderr():
                last_layer = learner_func(pretrained_model)
        except Exception as e:
            t.failed = True
            t.msg = f"There was an error evaluating {function_name} function"
            t.want = "No exceptions"
            t.got = f"{e}"
            return [t]

        t = test_case()
        if not tf.keras.backend.is_keras_tensor(last_layer):
            t.failed = True
            t.msg = f"Got wrong output type for {function_name} function"
            t.want = "a KerasTensor object"
            t.got = type(last_layer)
            return [t]

        t = test_case()
        shape = last_layer.shape
        if shape != (None, 7, 7, 768):
            t.failed = True
            t.msg = "Incorrect shape for output of mixed7 layer"
            t.want = (None, 7, 7, 768)
            t.got = shape
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_create_final_model(learner_func, pretrained_model, last_output):
    def g():
        function_name = "create_final_model"

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
            model = learner_func(pretrained_model, last_output)
        except Exception as e:
            t.failed = True
            t.msg = f"There was an error evaluating {function_name} function"
            t.want = "No exceptions"
            t.got = f"{e}"
            return [t]

        random_images = tf.random.uniform((32, 150, 150, 3))
        random_labels = tf.zeros((32,))

        try:
            with suppress_stdout_stderr():
                model.evaluate(random_images, random_labels)
        except Exception as e:
            t.failed = True
            t.msg = "your model could not be used for inference"
            t.want = "No exceptions"
            t.got = f"{e}"
            return [t]

        t = test_case()
        if isinstance(model.loss, tf.keras.losses.Loss):
            if not isinstance(model.loss, tf.keras.losses.BinaryCrossentropy):
                t.failed = True
                t.msg = "incorrect loss function used for model"
                t.want = "and instance of tf.keras.losses.BinaryCrossentropy"
                t.got = model.loss

        elif isinstance(model.loss, str):
            if "binary_crossentropy" not in model.loss:
                t.failed = True
                t.msg = "incorrect loss function used for model"
                t.want = "binary_crossentropy"
                t.got = model.loss
        else:
            t.failed = True
            t.msg = "loss function should be a string or a class from tf.keras.losses"
            t.want = "a string or a class from tf.keras.losses"
            t.got = type(model.loss)
        cases.append(t)

        t = test_case()
        if not isinstance(model.input, tf.keras.KerasTensor):
            t.failed = True
            t.msg = "the input of your model has incorrect type"
            t.want = "a tf.keras.KerasTensor"
            t.got = type(model.input)
            return [t]

        t = test_case()
        input_shape = model.input.shape
        if not input_shape == (None, 150, 150, 3):
            t.failed = True
            t.msg = "Got a wrong input shape for the final model."
            t.want = (None, 150, 150, 3)
            t.got = input_shape
        cases.append(t)

        t = test_case()
        if not model.output.shape == (None, 1):
            t.failed = True
            t.msg = "wrong output shape for model"
            t.want = (None, 1)
            t.got = model.output.shape
        cases.append(t)

        t = test_case()
        if not model.get_compile_config()["metrics"] == ["accuracy"]:
            t.failed = True
            t.msg = "missing accuracy metric when compiling model"
            t.want = "'accuracy' defined as a metric"
            t.got = model.get_compile_config()["metrics"]
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
