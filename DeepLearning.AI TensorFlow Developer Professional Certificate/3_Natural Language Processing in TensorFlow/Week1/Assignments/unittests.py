from dlai_grader.grading import test_case, print_feedback
import tensorflow as tf
import numpy as np
from types import FunctionType


def test_parse_data_from_file(learner_func):
    def g():
        function_name = "parse_data_from_file"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        filename = "./data/bbc-text.csv"
        returned = learner_func(filename)

        t = test_case()
        if not isinstance(returned, tuple):
            t.failed = True
            t.msg = f"{function_name} should return a tuple of sentences, labels"
            t.want = tuple
            t.got = type(returned)
            return [t]

        sentences, labels = returned

        t = test_case()
        if not isinstance(sentences, list):
            t.failed = True
            t.msg = f"the first item (sentences) returned by {function_name} should be a list"
            t.want = list
            t.got = type(sentences)
            return [t]

        t = test_case()
        if not isinstance(sentences[0], str):
            t.failed = True
            t.msg = "sentences should be a list of strings. Testing first element of sentences"
            t.want = str
            t.got = type(sentences[0])
            return [t]

        t = test_case()
        if not isinstance(labels, list):
            t.failed = True
            t.msg = (
                f"the second item (labels) returned by {function_name} should be a list"
            )
            t.want = list
            t.got = type(labels)
            return [t]

        t = test_case()
        if not isinstance(labels[0], str):
            t.failed = True
            t.msg = (
                "labels should be a list of strings. Testing first element of labels"
            )
            t.want = str
            t.got = type(labels[0])
            return [t]

        t = test_case()
        if len(sentences) != 2225:
            t.failed = True
            t.msg = "Incorrect number of sentences for the full dataset. Make sure you didn't include the header."
            t.want = 2225
            t.got = len(sentences)
        cases.append(t)

        t = test_case()
        if len(labels) != 2225:
            t.failed = True
            t.msg = "Incorrect number of labels for the full dataset. Make sure you didn't include the header."
            t.want = 2225
            t.got = len(labels)
        cases.append(t)

        sentences, labels = learner_func("./data/bbc-text-minimal.csv")

        t = test_case()
        if len(sentences) != 5:
            t.failed = True
            t.msg = "Incorrect number of sentences for the miniature dataset. Make sure you didn't hardcode the path to the csv file."
            t.want = 5
            t.got = len(sentences)
        cases.append(t)

        t = test_case()
        if len(labels) != 5:
            t.failed = True
            t.msg = "Incorrect number of labels for the miniature dataset. Make sure you didn't hardcode the path to the csv file."
            t.want = 5
            t.got = len(labels)
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_standardize_func(learner_func):
    def g():
        function_name = "standardize_func"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        expected_cases = [
            ("HELLO", "hello"),
            ("HEllO mY FriEnds", "hello friends"),
            ("hello    again   FRIENDS", "hello friends"),
            (
                "Hello! We're just about to see this function in action =)",
                "hello! just see function action =)",
            ),
            (
                "tigers wary of farrell  gamble  leicester say they will not be rushed into making a bid for andy farrell should the great britain rugby league",
                "tigers wary farrell gamble leicester say will not rushed making bid andy farrell great britain rugby league",
            ),
        ]

        for raw, sol_str in expected_cases:
            t = test_case()
            try:
                learner_str = learner_func(raw)
            except Exception as e:
                t.failed = True
                t.msg = f"There was an error evaluating the {function_name} function."
                t.want = "No exceptions"
                t.got = f"{str(e)}"
                return [t]

            t = test_case()
            if not isinstance(learner_str, str):
                t.failed = True
                t.msg = f"incorrect type returned by {function_name}"
                t.want = str
                t.got = type(learner_str)
                return [t]

            t = test_case()
            if learner_str != sol_str:
                t.failed = True
                t.msg = f"incorrect type standardization for string:\n'{raw}'"
                t.want = sol_str
                t.got = learner_str
            cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_fit_vectorizer(learner_func):
    def g():
        function_name = "fit_vectorizer"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        sentences = ["cats cool", "cats best cool"]
        vectorize_layer = learner_func(sentences)

        t = test_case()
        if not isinstance(vectorize_layer, tf.keras.layers.TextVectorization):
            t.failed = True
            t.msg = f"incorrect type returned by {function_name}"
            t.want = tf.keras.layers.TextVectorization
            t.got = type(vectorize_layer)
            return [t]

        vocabulary = vectorize_layer.get_vocabulary()
        t = test_case()
        if len(vocabulary) != 5:
            t.failed = True
            t.msg = f"The number of tokens in the vocabulary is not correct for sentences:\n{sentences}.\nMake sure you correctly fit it on the texts."
            t.want = 5
            t.got = len(vocabulary)
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)


def test_fit_label_encoder(learner_func):
    def g():
        function_name = "fit_label_encoder"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]

        labels = ["cat", "dog", "cat", "cat", "mouse"]
        label_encoder = learner_func(labels)

        t = test_case()
        if not isinstance(label_encoder, tf.keras.layers.StringLookup):
            t.failed = True
            t.msg = f"incorrect type returned by {function_name}"
            t.want = tf.keras.layers.StringLookup
            t.got = type(label_encoder)
            return [t]

        label_sequences = label_encoder(labels)

        t = test_case()
        if not tf.is_tensor(label_sequences):
            t.failed = True
            t.msg = "label_sequences has incorrect type"
            t.want = tf.Tensor
            t.got = type(label_sequences)
            return [t]

        vocabulary = label_encoder.get_vocabulary()

        t = test_case()
        if not isinstance(vocabulary, list):
            t.failed = True
            t.msg = "vocabulary has incorrect type"
            t.want = list
            t.got = type(vocabulary)
            return [t]

        t = test_case()
        if len(label_sequences) != len(labels):
            t.failed = True
            t.msg = "the length of label_sequences did not correspond to the length of labels when using 5 labels"
            t.want = len(labels)
            t.got = len(label_sequences)
        cases.append(t)

        t = test_case()
        if len(vocabulary) != len(set(labels)):
            t.failed = True
            t.msg = "the number of entries in the vocabulary did not correspond to the number of unique labels when using 5 labels (3 unique). Check the vocabulary does not include a OOV token"
            t.want = len(set(labels))
            t.got = len(vocabulary)
        cases.append(t)

        return cases

    cases = g()
    print_feedback(cases)
