from dlai_grader.grading import test_case, print_feedback
from types import FunctionType
from collections import defaultdict
import json
import random
import os
import multiprocessing
import time

## Do NOT modify this class.
class Node:
	def __init__(self, data):
		self.data = data
		self.prev = None
		self.next = None

# Deserialize graph from JSON
# The graph has 20 nodes, numbered 0-19
def dg(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return defaultdict(list, {int(k): v for k, v in data.items()})

def test_is_palindrome_fixed(learner_func):
    def g():
        function_name = "is_palindrome_fixed"

        cases = []

        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]
        
        test_cases = [("I like bread", False),
                      ("There's a reason for that", False),
                      ("Draw, O coward!", True),
                      ("Step on no pets.", True)
                        ]
        
        for sentence, result in test_cases:
            t = test_case()
            try:
                res = learner_func(sentence)
            except Exception as e:
                t.failed = True
                t.msg = f"{function_name} thrown an exception when sentence = \"{sentence}\". Aborting unittest"
                t.want = f"{function_name} should run for any string"
                t.got = f"Exception thrown was: {e}"     
                return [t]
            if res != result:
                t.failed = True
                t.msg = f"Incorrect output for sentence \"{sentence}\""
                t.want = f"{result}"
                t.got = f"{res}"
            cases.append(t)
        return cases

    cases = g()
    print_feedback(cases)


def gr(n, l, f):a={str(i): [] for i in range(n)};b=[(i, random.randint(1, 10)) for i in range(1, n) if i not in l];c=[(i, j, random.randint(1, 10)) for i in range(1, n) for j in range(i + 1, n) if i not in l and j not in l];[a["0"].append([i, w]) or a[str(i)].append([0, w]) for i, w in b];[a[str(i)].append([j, w]) or a[str(j)].append([i, w]) for i, j, w in c];[a[str(i)].append([j, w]) for i in l for j in range(1, n) if j not in l and j != 0 for w in [random.randint(1, 10)]];open(f, 'w').write(json.dumps(a, indent=4))



def test_dijkstra_fixed(learner_func):
    import heapq
    def g():
        function_name = "dijkstra_fixed"

        cases = []
        t = test_case()
        if not isinstance(learner_func, FunctionType):
            t.failed = True
            t.msg = f"{function_name} has incorrect type"
            t.want = FunctionType
            t.got = type(learner_func)
            return [t]
        tcs = [[6, 18, 14], [1, 2, 1, 1, 7, 5, 16, 11, 11, 5], [17, 8, 18, 1, 13, 17, 10], [9, 16, 19, 15, 6, 5, 2, 4, 10, 8, 5], [16, 12, 16, 5, 9, 6, 19, 6, 6, 18, 4, 3, 19, 4], [2, 1, 7], [16, 15], [8, 17, 16, 8, 14, 14, 6, 15, 5, 18, 17, 14, 2, 9, 15], []]
        tcs = [list(set(x)) for x in tcs]

        
        for l in tcs:
            k = len(l)
            gr(20, l, 'p')
            g = dg('p')
            os.remove('p')
            t = test_case()
            try:
                d, valid_path = learner_func(g,0)
                if (not isinstance(d,dict)) or (not isinstance(valid_path, bool)):
                    t.failed = True
                    t.msg = f"{learner_func} has incorrect output types."
                    t.want = f"First output must be a dictionary and second output must be a boolean"
                    t.got = f"Type of first output: {type(d)}. Type of second output: {type(valid_path)}"
                    return [t]
            except Exception as e:
                t.failed = True
                t.msg = f"{function_name} thrown an exception with graph = {g}. Aborting unittest"
                t.want = f"{function_name} must run without exceptions"
                t.got = f"{e}"
                return [t]
            for node in l:
                t = test_case()
                if node not in d.keys():
                    t.failed = True
                    t.msg = f"Node {node} is not present in distances dictionary"
                    t.want = f"Every node must be present in the distance dictionary"
                elif d[node] != float('inf'):
                    t.failed = True
                    t.msg = f"Node {node} should have infinite distance for graph = {g}"
                    t.want = f"Distance from 0 to {node} must be infinite"
                    t.got = f"Distance is {d[node]}"
                cases.append(t)
            t = test_case()
            if k != 0 and valid_path:
                t.failed = True
                t.msg = f"{learner_func} should return False for graph = {g}"
                t.want = f"{False}"
                t.got = f"{valid_path}"
            elif k == 0 and (not valid_path):
                t.failed = True
                t.msg = f"{function_name} should return True for graph = {g}"
                t.want = f"{True}"
                t.got = f"{valid_path}"
            cases.append(t)
        return cases
    
    cases = g()
    print_feedback(cases)


def test_StackFixed(learner_func):
    def g():
        function_name = "StackFixed"

        attrs = ['push', 'pop', 'peek', 'is_empty', 'size']

        cases = []
        t = test_case()
        for attr in attrs:
            if not hasattr(learner_func, attr):
                t.failed = True
                t.msg = f"{function_name} does not have {attr} method. Aborting unittests"
                return [t]
        
        s = learner_func()
        vals = [1,4,6,1,4,3,5,6]
        success = False
        for val in vals:
            s.push(val)
        t = test_case()
        for _ in range(len(vals)+1):
            try:
                s.pop()
            except IndexError:
                success = True
        if not success:
            t.failed = True
            t.msg = f"Your stack's .pop method does not work as the list .pop method"
            t.expected = "An Exception of the right type when popping from an empty stack"
            t.got = "The .pop didn't throw an exception OR it thrown the wrong type of exception"
        cases.append(t)
        t = test_case()
        success = False
        try:
            s.peek()
        except IndexError:
            success =True
        if not success:
            t.failed = True
            t.msg = f"Your stack's .peek method does not work as the respective way of getting the last element of an empty list"
            t.want = "An execution analogous to the list execution when you try to get the last element of an empty list"
            t.got = "Your execution didn't throw an Exception OR it thrown a differente type of exception"
        cases.append(t)

        return cases
    cases = g()
    print_feedback(cases)
        
def test_DoublyLinkedListFixed(learner_func):
    def g():
        function_name = "DoublyLinkedListFixed"

        attrs = ['add_node', 'link_nodes', 'traverse']

        cases = []
        t = test_case()
        for attr in attrs:
            if not hasattr(learner_func, attr):
                t.failed = True
                t.msg = f"{function_name} does not have {attr} method. Aborting unittests"
                return [t]
        
        s = learner_func()
        vals = [1,5,6,7,8]
        for val in vals:
            s.add_node(val)
        s.link_nodes(s.tail, s.head)
        t = test_case()
        time_limit = 1
        def helper(queue,func):
            out = func()
            queue.put(out)
            return
        t = test_case()
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=helper, name="traverse", args=(q,s.traverse))
        p.start()
        time.sleep(time_limit)
        if p.is_alive():
            p.terminate()
            t.failed = True
            t.msg = "The `.traverse` method is executing for an excessively long time, suggesting it might be stuck in an infinite loop. Execution will be aborted. Investigate when your linked list has the last node pointing to the first one"
        else:
            p.join()
            nodes = q.get()
            nodes = [x.data for x in nodes]
            if nodes != [1,5,6,7,8]:
                t.failed = True
                t.msg = f"Incorrect output for method .traverse when the last node points to the first one."
                t.want = [1,5,6,7,8]
                t.got = nodes
        cases.append(t)
        return cases
    cases = g()
    print_feedback(cases)
        
         