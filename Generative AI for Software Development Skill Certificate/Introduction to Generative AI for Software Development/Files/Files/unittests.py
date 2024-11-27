import numpy as np
from dlai_grader.grading import test_case, print_feedback
from types import FunctionType
from dlai_grader.io import suppress_stdout_stderr
import multiprocessing
import time
import random
import joblib 

def test_shortest_path(Graph):
    def g():
        function_name = "shortest_path"
        cases = []

        # Check if shortest_path method exists
        t = test_case()
        if not hasattr(Graph, 'shortest_path'):
            t.failed = True
            t.msg = f"Your Graph class does not contain a method called {function_name}"
            t.want = f"A Graph with a method called {function_name}"
            t.got = f"No {function_name} method detected"
            return [t]

        # Exeuction time limit (seconds)
        time_limit = 0.5
        # Random seed to 
        random.seed(42)
        test_cases = [(654, 114), (25, 759), (281, 250)]
        # Loads the graph.graph dictionary, this speeds up testing as there is no need to generate the graph
        graph_schema = joblib.load("data/shortest_path_data.joblib")
        solutions = [31, 31, 33, 36, 23, 35, 31, 26, 34]
        def helper(queue,func, arg):
            out = func(*arg)
            queue.put(out)
            return
        random.seed(42)
        count = 0 # This is just to print correctly the test number to the learners as there is a nested for loop.
        # For each graph, loads the learner's Graph class and runs it. If it exceeds time_limit seconds, break it and return as a failed test case.
        # The multiprocessing is necessary to be able to stop a function while it is running.
        for i,schema in enumerate(graph_schema):
            graph = Graph()
            graph.graph = schema
            for case in test_cases:
                t = test_case()
                q = multiprocessing.Queue()
                p = multiprocessing.Process(target=helper, name="shortest_path", args=(q, graph.shortest_path, case))
                p.start()
                time.sleep(time_limit)
                if p.is_alive():
                    p.terminate()
                    t.failed = True
                    t.msg = f"Exceeded time execution limit for path between nodes {case[0]} and {case[1]} in a graph. To replicate the graph, you may run generate_graph(nodes = 1000, edges = 100, seed = {42+i})"
                    t.want =  f"shortest_path method must run in less than 0.5 seconds"
                    t.got = "Time execution exceeded 0.5 seconds"
                else:
                    p.join()
                    dist, path = q.get()
                    if dist != solutions[count]:
                        t.failed = True
                        t.msg = f"Failed to find the optimal solution for path between nodes {case[0]} and {case[1]} in a graph. To replicate the graph, you may run generate_graph(nodes = 1000, edges = 100, seed = {42+i}), index = {i}"
                        t.want = solutions[count]
                        t.got = dist
                count+=1
                cases.append(t)

        return cases
    cases = g()
    print_feedback(cases)
    
def test_tsp_small_graph(Graph):
    def g():
        function_name = "tsp_small_graph"
        cases = []

        # Check if shortest_path method exists.
        t = test_case()
        if not hasattr(Graph, 'tsp_small_graph'):
            t.failed = True
            t.msg = f"Your Graph class does not contain a method called {function_name}"
            t.want = f"A Graph with a method called {function_name}"
            t.got = f"No {function_name} method detected"
            return [t]

        # Exeuction time limit (seconds)
        time_limit = 1
        solutions = [799, 893, 978, 776, 1394]
        # Loads the graph.graph dictionary, this speeds up testing as there is no need to generate the graph
        graph_schema = joblib.load('data/tsp_small_graph_data.joblib')
        # This function helps in getting the output from the multiprocessing.Process class
        def helper(queue,func, start):
            out = func(start)
            queue.put(out)
            return
        random.seed(42)
        # For each graph, loads the learner's Graph class and runs it. If it exceeds time_limit seconds, break it and return as a failed test case.
        # The multiprocessing is necessary to be able to stop a function while it is running.
        for i,schema in enumerate(graph_schema):
            graph = Graph()
            graph.graph = schema
            t = test_case()
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=helper, name="tsp_small_graph", args=(q,graph.tsp_small_graph, 0))
            p.start()
            time.sleep(time_limit)
            if p.is_alive():
                p.terminate()
                t.failed = True
                t.msg = f"Exceeded time execution limit for a tour starting in node 0. To replicate the graph, you may run generate_graph(nodes = 10, complete = True, seed = {42+i})"
                t.want =  f"shortest_path method must run in less than {time_limit} seconds"
                t.got = f"Time execution exceeded {time_limit} seconds"
            else:
                p.join()
                dist, path = q.get()
                if dist != solutions[i]:
                    t.failed = True
                    t.msg = f"Failed to find the optimal solution for a path starting in node 0. To replicate the graph, you may run generate_graph(nodes = 10, complete = True, seed = {42+i})"
                    t.want = solutions[i]
                    t.got = dist
            cases.append(t)
            
        return cases
    cases = g()
    print_feedback(cases)

def test_tsp_large_graph(Graph):
    def g():
        function_name = "tsp_large_graph"
        cases = []

        # Check if shortest_path method exists
        t = test_case()
        if not hasattr(Graph, 'tsp_large_graph'):
            t.failed = True
            t.msg = f"Your Graph class does not contain a method called {function_name}"
            t.want = f"A Graph with a method called {function_name}"
            t.got = f"No {function_name} method detected"
            return [t]

        # Exeuction time limit (seconds)
        time_limit = 0.5
        solutions = [4367, 4774, 5217, 4357, 4613]
        # Loads the graph.graph dictionary, this speeds up testing as there is no need to generate the graph
        graph_schema = joblib.load("data/tsp_large_graph_data.joblib")
        # This function helps in getting the output from the multiprocessing.Process
        def helper(queue,func, start):
            out = func(start)
            queue.put(out)
            return
        random.seed(42)
        # For each graph, loads the learner's Graph class and runs it. If it exceeds time_limit seconds, break it and return as a failed test case.
        # The multiprocessing is necessary to be able to stop a function while it is running.
        for i,schema in enumerate(graph_schema):
            graph = Graph()
            graph.graph = schema
            t = test_case()
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=helper, name="tsp_large_graph", args=(q,graph.tsp_large_graph, 0))
            p.start()
            time.sleep(time_limit)
            if p.is_alive():
                p.terminate()
                t.failed = True
                t.msg = f"Exceeded time execution limit for a tour starting in node 0. To replicate the graph, you may run generate_graph(nodes = 1000, complete = True, seed = {42+i})"
                t.want =  f"{function_name} method must run in less than 0.5 seconds"
                t.got = f"Time execution exceeded {time_limit} seconds"
            else:
                p.join()
                dist, path = q.get()
                if dist > solutions[i]*1.2:
                    t.failed = True
                    t.msg = f"Failed to find the optimal solution for a path starting in node 0. To replicate the graph, you may run generate_graph(nodes = 1000, complete = True, seed = {42+i})"
                    t.want = solutions[i]
                    t.got = dist
            cases.append(t)
        return cases
    cases = g()
    print_feedback(cases)


def test_tsp_medium_graph(Graph):
    def g():
        function_name = "tsp_medium_graph"
        cases = []

        # Check if shortest_path method exists
        t = test_case()
        if not hasattr(Graph, 'tsp_medium_graph'):
            t.failed = True
            t.msg = f"Your Graph class does not contain a method called {function_name}"
            t.want = f"A Graph with a method called {function_name}"
            t.got = f"No {function_name} method detected"
            return [t]

        # Exeuction time limit (seconds)
        time_limit = 1.5
        solutions = [3855, 3554, 3665, 3192, 3760, 3786, 3669, 3668, 4362, 4148]
        # Loads the graph.graph dictionary, this speeds up testing as there is no need to generate the graph
        graph_schema = joblib.load("data/tsp_medium_graph.joblib")
        # This function helps in getting the output from the multiprocessing.Process
        def helper(queue,func, start):
            out = func(start)
            queue.put(out)
        random.seed(42)
        # For each graph, loads the learner's Graph class and runs it. If it exceeds time_limit seconds, break it and return as a failed test case.
        # The multiprocessing is necessary to be able to stop a function while it is running.
        for i,schema in enumerate(graph_schema):
            graph = Graph()
            graph.graph = schema
            t = test_case()
            q = multiprocessing.Queue()
            p = multiprocessing.Process(target=helper, name="tsp_medium_graph", args=(q,graph.tsp_medium_graph, 0))
            p.start()
            time.sleep(time_limit)
            if p.is_alive():
                p.terminate()
                t.failed = True
                t.msg = f"Exceeded time execution limit for a tour starting in node 0. To replicate the graph, you may run generate_graph(nodes = 300, complete = True, seed = {42+i})"
                t.want =  f"{function_name} method must run in less than {time_limit} seconds"
                t.got = f"Time execution exceeded {time_limit} seconds"
            else:
                p.join()
                dist, path = q.get()
                if round(dist/solutions[i],2) > 1.76:
                    t.failed = True
                    t.msg = f"Failed to find a solution a solution closest to the optimal solution. To replicate the graph, you may run generate_graph(nodes = 300, complete = True, seed = {42+i})"
                    t.want = 'Solution no greater than 76% of Nearest Neighbor.'
                    t.got = f"For the graph starting at node 0, the target path distance to beat is {solutions[i]}. Your algorithm returned a distance of {dist}, greater than 76%."
            cases.append(t)
        return cases
    cases = g()
    print_feedback(cases)
        
    