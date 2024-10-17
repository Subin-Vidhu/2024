# Basic Unpacking
a, b, c = [1, 2, 3]
print(f"a: {a}, b: {b}, c: {c}\n")

# Extended Iterable Unpacking with *
a, *b, c = [1, 2, 3, 4, 5]
print(f"a: {a}, b: {b}, c: {c}\n")

# Ignoring Values
_, _, c = [1, 2, 3]
print(f"c: {c}\n")

# Unpacking Nested Structures
data = ("Alice", (25, "Engineer"))
# name, age, profession = data # not enough values to unpack error
# '''
#     name, age, profession = data # not enough values to unpack error
# ValueError: not enough values to unpack (expected 3, got 2)
# '''
try:
    name, age, profession = data
except ValueError as e:
    print(f"Error: {e}\n")
    name, (age, profession) = data
    print(f"name: {name}, age: {age}, profession: {profession}\n")


# Unpacking in Function Arguments
def print_names(*names):
    for name in names:
        print(name)


print_names("Alice", "Bob", "Charlie")

# Combining Lists with Unpacking
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]
print(*list1)
print(f"Combined List: {combined}\n")

# Unpacking Dictionaries with **
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
combined_dict = {**dict1, **dict2}
print(f"Combined Dictionary: {combined_dict}\n")

# Swapping Variables Using Unpacking
x = 10
y = 20
print(f"Before Swap - x: {x}, y: {y}")
x, y = y, x
print(f"After Swap - x: {x}, y: {y}\n")
