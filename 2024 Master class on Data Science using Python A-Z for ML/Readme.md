Notes on Telegram. Certificate on Drive.

Python Crash Course

1. Variables in Python
```
 -  a container which can hold a value inside it. (diff types - int, double, float, string, boolean)
 -  swapping(a,b = b,a [can also be done with a temp var])
 -  multiple assignments (a, b = 1,2)
```
 2. Conditionals 
```
  -  if condition:
               #statement

  -  if condition:
               #statement
     else:
             #statement
  -  Nested if statements
  -  elif statements

     if condition:
               #statement
     elif condition:
               #statement
     else:
             #statement
 -  While loop
   
    while expression:
                  statement(s)
 -  For loop
    for var in iterable:
          statement(s)
 -  For else
    for var in iterable:
                  statement(s)
    else:
             statement(s)
```
3. Break and Continue
```
 -  break : break out of the loop 
 -  continue: skip the condition/ iteration
```
4. Containers 
```
 -  mutable vs immutable
 -  ordered vs unordered
 -  indexible vs non-indexible
```

```
 -List: ordered sequence of objects
 []
 can be of any type
 mutable
 list() -  creates an empty list
 list indexing starts at 0, ie, the first element is list[0]
 list slicing - use :
 list[::-1] - reverses the entire list
 list[1] = "a", updates the value in the first position in the list
 list.append("c") - appends a value to the end of the list
 list.extend([1,2,3]) - adds element to the list
 list.insert(0, "z") - inserts an element at a given position, so there will be a shift of the existing elements to the right of this entry
 list.pop() - last element gets removed
 list.count(1) - counts the number of times an item occurs in a list
 list.index(13) - returns the index of the first occurence
 list.reverse() - list gets reversed
 sorted(list) - returns sorted list, but doesnt modify the existing list [sorted(list, reverse = True), sorts in the reverse order(descending)]
 list.sort() - sorts the list and modifies it as well
 min(list) , max(list)
 del list[0] - the first element gets deleted
 list.clear - makes the list empty
 list2 = list1 (both the content and id same)
 list2 = list1.copy() (only the content remains the same, id differs) [to find id = id(list)]
 list.remove(99) - removes the first occurence of the value
 + - appends two lists
 * - repeats elements
 list comprehension - [x**2 for x in range(10)]
```
```
 Tuple: immutable
 ()
 indexing and slicing same as list
 tuple1 = 1,2,3 [Any comma-separated sequence of values defines a tuple]
 check for an item in tuple  - if value in tuple:
 tuple(start: end: jumpindex) [default jumpindex = 1]
 list(tuple) -  to convert the tuple into a list
 Unpacking tuples
```
```
 Set: unordered collection of items with no duplicates
{}
immutable
set() - creates an empty set
in - to check item
```
```
Dictionaries: containers where items are accessed by a key
{key:value}
{}/ dict() - creates an empty dictionary
New key:value pairs can be assigned using the = operator
dict.get(key) - returns none if no value exists
for key,value in dict.items():
                print(key, value)
```
             
5. Functions 
```   
  -  def <name> (<parameteres>):
                  """ doc string """
                  code

 -  def square(x):
           return(x**2)

 -  function exists as soon as the return statement is called.

```

- Data Handling Using Numpy
```
Module - file containing Python definitions and statements.

 - from math import pi
 - from math import *
 - import numpy as np
 
Creating and displaying 1D array:
 - np.array([1,2,3,4,5])

 - np.zeros(5)
 - np.ones(5)
 - np.sort(arr)
 - arr[start: stop: step]
 - mathematical operations on array [+,-,*,/]
 - searching for an element in array [np.where(arr == 4), np.where(arr%2 == 0) - Both returns the indexes as answer]
 - filtering an array [arr([True, False, True, False])]
 - arr.size [returns the size(total number of elements) of the array]
 
Creating and displaying 2D array:
 - np.array([[1,2,3],[4,5,6]])
 - ndim : returns the dimension of the array
 - arr.shape  : returns the order of the array
 - arr.reshape(6,2) : reshapes the order of the array(make sure that m*n is satisfied, ie, the new shape's product should equal the total number of elements)
 - np.eye(3) : identity matrix with order 3*3
 - np.arange(1,10) [start: stop: step]
 - np.linspace(1,10) [ evenly spaced numbers over a specified interval ][start: stop: step]
   eg: 
   np.linspace(1,10,10)
   Out[7]: array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9., 10.])

   np.linspace(1,10,5)
   Out[8]: array([ 1.  ,  3.25,  5.5 ,  7.75, 10.  ])

 - random array
   np.random.rand(5) : array that ranges from 0 to 1, [0,1)
   np.random.rand(3,4) : random matrix

 - diagonal matrix

   np.diag([1,2,3])
   Out:  array([[1, 0, 0],
          [0, 2, 0],
          [0, 0, 3]])

 - Flatten matrix [transform a matrix to a one dimensional numpy array]
   a
   Out: 
   array([[1, 2, 3],
          [4, 5, 6]])
   
   a.flatten()
   Out: array([1, 2, 3, 4, 5, 6])

 - trace [sum of the diagonal elements]
   a.trace / sum(a.diagonal())
   
 - transpose [rows as columns and columns as rows]
   np.transpose(a) / a.T / a.transpose()

 - Negative indexing to access elements in the array.
```


- Data Handling using Pandas
```
 - package of python for manipulating tables.
 - built on top of numpy, so efficient

 - datastructures: series(1D), dataframe(2D)
```

- Series
```
import pands as pd
pd.Series()

p = pd.Series([1,2,3,4,5])

p  
Out[15]: 
0    1
1    2
2    3
3    4
4    5
dtype: int64

p = pd.Series([1,2,3,4,5], index = ['a', 'b' , 'c', 'd', 'e'])

p
Out[19]: 
a    1
b    2
c    3
d    4
e    5
dtype: int64

 - combining series with numpy
   pd.Series(np.array([1,2,3,4,5]))

 - p.size : returns the number of elements in the series
 - p.mean()  - mean
 - p.max() -  max
 - p.min()  - min
 - p.sort_values() - to sort values [only values will be sorted, index remains the same]
 - p.unique() - returns the unique values in the series
 - p.nunique() - returns the number of unique values in the series
 - p.describe() - statistics summary
```

- Dataframe
```
pd.DataFrame() : creates an empty dataframe
pd.DataFrame(p) : dataframe from series


   import pandas as pd

   name = pd.Series(["R","V"])
   team = pd.Series(["A","B"])
   dic = {'Name':name, 'Team':team}

   df = pd.DataFrame(dic)
   print(df)
       Name Team
   0           R       A
   1           V       B

 - DataFrame from list of dictionaries
   
   import pandas as pd
l = [{'Name':"Subin", 'Team':"team A"}, {'Name':"Chippy", 'Team':"team B"}, {'Name':"Ant", 'Team':"team C"}]

df = pd.DataFrame(l)
print(df)
     Name    Team
0   Subin     team A
1  Chippy    team B
2     Ant        team C

 - df.iterrows()
 - df.iteritems()

 - df.columns = ['List1'] : to add a name to the column
 - df['List2'] = 20 , a new column with name List2 will be added to the dataframe with all their values as 20
 - del df['List2'] / df.pop('List2'): to delete that column
 - df.drop('List2', axis = 1) :  drops this particular column from the dataframe [axis = 1: drops column, axis = 0: drops rows]
 - .loc
 - pd.concat ...

```
Data Visualization using Matplotlib in python
```
 - can understand the data well when you visualize it. [plotting graphs]

 - line plot: plotting a line across x, y axis
 - bar plot: rectangular boxes
 - scatter plot: points scattered across the graph
 - pie plot: slices of pie
 - area plot: high and low areas
 - histogram: data remains distributed

 ```
 - Line plot
 ```
   import matplotlib.pyplot as plt
   x = [1,2,3]
   y = [10,20,30]
   plt.plot(x,y)
   plt.title("Heading")
   plt.xlabel("x-axis")
   plt.ylabel("y-axis")
   plt.show()
   ```
- Bar plot
```
   import matplotlib.pyplot as plt
   x = [1,2,3]
   y = [10,20,30]
   plt.bar(x,y)
   plt.title("Heading")
   plt.xlabel("x-axis")
   plt.ylabel("y-axis")
   plt.show()
   ```
- Scatter plot
```
   import matplotlib.pyplot as plt
   x = [1,2,3]
   y = [10,20,30]
   plt.scatter(x,y)
   plt.title("Heading")
   plt.xlabel("x-axis")
   plt.ylabel("y-axis")
   plt.show()
   ```
- Histograms 
```
  A histogram is a graph showing frequency distributions.
  It is a graph showing the number of observations within each given interval.
  plt.hist([1,2,3], bins=[1,2,3])
  ```
 - Pie
   ```
    x = [1,2,3,4]
    e = (0.3,0,0,0)
    plt.pie(x, explode = e)
    ```
 - 3D plot
 ```
   fig = plt.figure()
   ax = plt.axes(projection = '3d')
   [just a plot with no values inside it]

   fig = plt.figure()
   ax = plt.axes(projection = '3d')
   ax.plot3D([1,2,3],[4,5,6],[7,8,9]) #line graph
```

Data Visualization using Seaborn in python

- data visualization library based on matplotlib
```
   import pandas as pd
   import numpy as np
   import matplotlib.pyplot as plt
   import seaborn
   %matplotlib inline
   df = seaborn.load_dataset("filename")
   df.head() [first 5 rows]
   df.tail() [last 5 rows]
   ```
 - swarm plot
 ```
 
   type of scatter plot used for representing categorical values
   seaborn.swarmplot(data = df)
   ```
 - violin plot
 ```
   statistical representation of numerical data
   seaborn.violinplot(data = df)
   ```
 - Facetgrid

 - Heatmap
 ```
   graphical representation of data using colors to visualize the matrix
   seaborn.heatmap(data)
```
