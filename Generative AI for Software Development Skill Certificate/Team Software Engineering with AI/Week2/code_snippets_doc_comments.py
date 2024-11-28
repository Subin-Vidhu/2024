#################################################  Example 1
def calculate_area(radius):
    pi = 3.14159
    return pi * radius * radius

# generate a documentation comment for the calculate_area function
def calculate_area(radius):
    """
    Calculate the area of a circle given its radius.

    This function uses the formula A = πr² to compute the area,
    where A is the area and r is the radius of the circle. The value
    of π is approximated as 3.14159.

    Parameters:
    radius (float): The radius of the circle. Must be a non-negative number.

    Returns:
    float: The area of the circle.

    Raises:
    ValueError: If the radius is negative.

    Example:
    >>> calculate_area(5)
    78.53975
    """
    pi = 3.14159
    return pi * radius * radius

#################################################### Example 2
def find_max(numbers):
    max_number = numbers[0]
    for number in numbers:
        if number > max_number:
            max_number = number
    return max_number

##################
def find_max(numbers):
    """
    Find the maximum number in a list of numbers.

    This function iterates through a list of numbers and identifies
    the maximum value. It assumes the list contains at least one element.

    Parameters:
    numbers (list of int/float): A list of numerical values. The list must
    contain at least one element.

    Returns:
    int/float: The maximum number in the list.

    Raises:
    ValueError: If the list is empty.

    Example:
    >>> find_max([3, 5, 7, 2, 8])
    8
    """
    if not numbers:
        raise ValueError("The list is empty.")
    
    max_number = numbers[0]
    for number in numbers:
        if number > max_number:
            max_number = number
    return max_number

################################################ Example 3
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# generate a documentation comment for the bubble_sort function. This time, instruct the LLM to write the comment for a specific audience, for example a novice coder or a developer who usually works in C++ of Java.

def bubble_sort(arr):
    """
    Sort a list of elements using the bubble sort algorithm.

    This function is designed for developers who are familiar with 
    C++ or Java and are transitioning to Python. Bubble sort is a simple 
    sorting algorithm that repeatedly steps through the list, compares 
    adjacent elements, and swaps them if they are in the wrong order. 
    The process is repeated until the list is sorted.

    Parameters:
    arr (list of int/float): A list of numerical values to be sorted.

    Returns:
    list of int/float: The sorted list of numbers in ascending order.

    Time Complexity:
    The worst-case and average time complexity of bubble sort is O(n^2),
    where n is the number of elements in the list.

    Example:
    >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
    [11, 12, 22, 25, 34, 64, 90]

    Note:
    In Python, swapping elements is easily done using tuple unpacking 
    (arr[j], arr[j+1] = arr[j+1], arr[j]), which might be different 
    from the swap operations you are used to in C++ or Java.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# refactor the documentation comment it just wrote into the ReST style.
def bubble_sort(arr):
    """
    Sort a list of elements using the bubble sort algorithm.

    This function is designed for developers who are familiar with 
    C++ or Java and are transitioning to Python. Bubble sort is a simple 
    sorting algorithm that repeatedly steps through the list, compares 
    adjacent elements, and swaps them if they are in the wrong order. 
    The process is repeated until the list is sorted.

    :param arr: A list of numerical values to be sorted.
    :type arr: list of int/float

    :return: The sorted list of numbers in ascending order.
    :rtype: list of int/float

    :Time Complexity: The worst-case and average time complexity of bubble sort is O(n^2),
                      where n is the number of elements in the list.

    :Example:

    >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
    [11, 12, 22, 25, 34, 64, 90]

    .. note::
        In Python, swapping elements is easily done using tuple unpacking 
        (``arr[j], arr[j+1] = arr[j+1], arr[j]``), which might be different 
        from the swap operations you are used to in C++ or Java.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr