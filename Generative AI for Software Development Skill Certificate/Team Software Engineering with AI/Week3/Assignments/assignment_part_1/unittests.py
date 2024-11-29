#from dlai_grader.grading import test_case, print_feedback
from types import FunctionType
#from dlai_grader.io import suppress_stdout_stderr

class test_case:
	def __init__(self):
		self.msg = ""
		self.want = None
		self.got = None
		self.failed = False


def print_feedback(test_cases) -> None:
    """Prints feedback of public unit tests within notebook.

    Args:
        test_cases (List[test_case]): List of public test cases.
    """
    failed_cases = [t for t in test_cases if t.failed]
    feedback_msg = "\033[92m All tests passed!\033[30m"

    if failed_cases:
        feedback_msg = ""
        for failed_case in failed_cases:
            feedback_msg += f"\033[91mFailed test case: {failed_case.msg}.\nExpected: {failed_case.want}\nGot: {failed_case.got}\033[30m\n\n"

    print(feedback_msg)
	
def test_magic_summation_solution(learner_func):
    def g():
        function_name = "magic_summation"
        cases = []

        if not isinstance(learner_func, FunctionType):
            t = test_case()
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]
        
        n, seed, expected = 30, 10, 46
        try:
            result = learner_func(n, seed=seed)
            t = test_case()
        except Exception as e:
            t = test_case()
            t.failed = True
            t.msg = f"{function_name} thrown an exception. Review your syntax and make sure it is properly converted to Python 3"
            t.want = f"{function_name} must run without exceptions"
            t.got = f"Exception raised:\n\t{e}"
            return [t]
        
        if result != expected:
            t = test_case()
            if isinstance(result, float):
                t.failed = True
                t.msg = f"{function_name} executed properly, but output is incorrect for parameters n = {n} and seed = {seed}. Note that the behavior of the division operator changed from Python 2 to Python 3. You should ask an LLM about it."
                t.want = f"{expected}"
                t.got = f"{result}"
                return [t]
            t.failed = True
            t.msg = f"{function_name} executed properly, but output is incorrect for parameters n = {n} and seed = {seed}"
            t.want = f"{expected}"
            t.got = f"{result}"
            return [t]
        
        cases.append(t)
        return cases
        
    cases = g()
    print_feedback(cases)


if __name__ == "__main__":
    import magic_summation
    test_magic_summation_solution(magic_summation.magic_summation)


        
         