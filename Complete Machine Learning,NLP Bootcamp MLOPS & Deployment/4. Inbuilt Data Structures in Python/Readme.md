### Data Structures in Python

- **Data Structures** are a way of organizing and storing data so that they can be accessed and worked with efficiently. They define the relationship between the data, and the operations that can be performed on the data. There are many different types of data structures, each with its own advantages and disadvantages. Some are better suited for specific tasks, while others are more versatile.

- Let's take a look at some of the most common data structures in Python:

1. **Lists**: A list is a collection of items that are ordered and changeable. Lists are defined by square brackets `[]` and can contain any type of data.

    - Example:
        ```python
        fruits = ["apple", "banana", "cherry"]
        print(fruits)
        ```

2. **Tuples**: A tuple is a collection of items that are ordered and unchangeable. Tuples are defined by parentheses `()` and can contain any type of data.

    - Example:
        ```python
        fruits = ("apple", "banana", "cherry")
        print(fruits)
        ```

3. **Sets**: A set is a collection of unique items that are unordered and unindexed. Sets are defined by curly braces `{}`.

    - Example:
        ```python
        fruits = {"apple", "banana", "cherry"}
        print(fruits)
        ```

4. **Dictionaries**: A dictionary is a collection of key-value pairs that are unordered and changeable. Dictionaries are defined by curly braces `{}` and consist of keys and values.

    - Example:
        ```python
        person = {
            "name": "John",
            "age": 30,
            "city": "New York"
        }
        print(person)
        ```

5. **Arrays**: Arrays are used to store multiple values in a single variable. They are similar to lists but can only contain values of the same type.

    - Example:
        ```python
        import array as arr
        numbers = arr.array('i', [1, 2, 3, 4, 5])
        print(numbers) # Output: array('i', [1, 2, 3, 4, 5])
        ```

6. **Stacks**: A stack is a collection of items that are ordered and changeable. Stacks follow the Last In First Out (LIFO) principle, where the last item added is the first one to be removed.

    - Example:
        ```python
        stack = []
        stack.append(1)
        stack.append(2)
        stack.append(3)
        print(stack) # Output: [1, 2, 3]
        stack.pop()
        print(stack) # Output: [1, 2]
        ```

7. **Queues**: A queue is a collection of items that are ordered and changeable. Queues follow the First In First Out (FIFO) principle, where the first item added is the first one to be removed.

    - Example:
        ```python
        from collections import deque
        queue = deque()
        queue.append(1)
        queue.append(2)
        queue.append(3)
        print(queue) # Output: deque([1, 2, 3])
        queue.popleft()
        print(queue) # Output: deque([2, 3])
        ```

8. **Linked Lists**: A linked list is a collection of items that are ordered and changeable. Each item in a linked list is called a node and contains a value and a reference to the next node in the list.

    - Example:
        ```python
        class Node:
            def __init__(self, data):
                self.data = data
                self.next = None

        class LinkedList:
            def __init__(self):
                self.head = None

            def append(self, data):
                new_node = Node(data)
                if self.head is None:
                    self.head = new_node
                    return
                last_node = self.head
                while last_node.next:
                    last_node = last_node.next
                last_node.next = new_node

            def print_list(self):
                current_node = self.head
                while current_node:
                    print(current_node.data)
                    current_node = current_node.next

        linked_list = LinkedList()
        linked_list.append(1)
        linked_list.append(2)
        linked_list.append(3)
        linked_list.print_list()
        ```

9. **Trees**: A tree is a hierarchical data structure that consists of nodes connected by edges. Each node in a tree has a parent node and zero or more child nodes.

    - Example:
        ```python
        class Node:
            def __init__(self, data):
                self.data = data
                self.left = None
                self.right = None

        root = Node(1)
        root.left = Node(2)
        root.right = Node(3)
        root.left.left = Node(4)
        root.left.right = Node(5)
        ```

10. **Graphs**: A graph is a collection of nodes connected by edges. Graphs can be directed or undirected, and can have weighted or unweighted edges.

    - Example:
        ```python
        graph = {
            "A": ["B", "C"],
            "B": ["A", "C", "D"],
            "C": ["A", "B", "D"],
            "D": ["B", "C"]
        }
        ```

11. **Hash Tables**: A hash table is a data structure that stores key-value pairs. It uses a hash function to map keys to values, allowing for fast retrieval of data.

    - Example:
        ```python
        hash_table = {}
        hash_table["name"] = "John"
        hash_table["age"] = 30
        hash_table["city"] = "New York"
        print(hash_table) # Output: {'name': 'John', 'age': 30, 'city': 'New York'}
        ```

12. **Heaps**: A heap is a binary tree data structure that satisfies the heap property. Heaps can be min-heaps or max-heaps, where the root node is the smallest or largest element in the tree, respectively.

    - Example:
        ```python
        import heapq
        heap = []
        heapq.heappush(heap, 1)
        heapq.heappush(heap, 2)
        heapq.heappush(heap, 3)
        print(heap) # Output: [1, 2, 3]
        heapq.heappop(heap)
        print(heap) # Output: [2, 3]
        ```

13. **Priority Queues**: A priority queue is a data structure that stores items with associated priorities. Items with higher priorities are dequeued before items with lower priorities.

    - Example:
        ```python
        import queue
        priority_queue = queue.PriorityQueue()
        priority_queue.put((1, "A"))
        priority_queue.put((3, "C"))
        priority_queue.put((2, "B"))
        while not priority_queue.empty():
            print(priority_queue.get()[1])
        ```

14. **Trie**: A trie is a tree data structure used to store a dynamic set of strings. Tries are commonly used in text processing applications.

    - Example:
        ```python
        class TrieNode:
            def __init__(self):
                self.children = {}
                self.is_end_of_word = False

        class Trie:
            def __init__(self):
                self.root = TrieNode()

            def insert(self, word):
                node = self.root
                for char in word:
                    if char not in node.children:
                        node.children[char] = TrieNode()
                    node = node.children[char]
                node.is_end_of_word = True

            def search(self, word):
                node = self.root
                for char in word:
                    if char not in node.children:
                        return False
                    node = node.children[char]
                return node.is_end_of_word

        trie = Trie()
        trie.insert("apple")
        trie.insert("banana")
        print(trie.search("apple")) # Output: True
        print(trie.search("orange")) # Output: False
        ```


