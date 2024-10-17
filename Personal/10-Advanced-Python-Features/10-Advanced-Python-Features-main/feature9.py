import itertools # itertools module provides a collection of functions to work with iterators, which are objects that can be iterated over (e.g., using a for loop).

# Infinite iterators
counter = itertools.count(
    start=10, step=2
)  # Infinite counter starting at 10, increasing by 2
print(next(counter))  # Output: 10
print(next(counter))  # Output: 12

# Cycling through a finite sequence infinitely
cycler = itertools.cycle(["A", "B", "C"])
print(next(cycler))  # Output: A
print(next(cycler))  # Output: B
print(next(cycler))  # Output: C
print(next(cycler))  # Output: A (repeats)

# Creating combinations of elements
combinations = itertools.combinations("ABC", 2)
print(list(combinations))  # Output: [('A', 'B'), ('A', 'C'), ('B', 'C')]

# Creating permutations of elements
permutations = itertools.permutations("ABC", 2)
print(list(permutations))  # Output: [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]