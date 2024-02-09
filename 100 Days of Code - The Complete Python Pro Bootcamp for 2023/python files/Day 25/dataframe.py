import pandas 
data=pandas.read_csv("100 Days of Code - The Complete Python Pro Bootcamp for 2023/python files/Day 25/weather-data.csv")

#TODO 1:To print entire table
# print(data)

#TODO 2:To print temp column of weather_data csv file
# print(data["temp"])
# OR
# print(data.temp)

#Pandas has 2 primary data structures-series and dataframe

#TODO 3:Checking datatype 
# print(type(data))  #This is a dataframe(In Pandas,entire table is called dataframe)
# print(type(data["temp"])) #This is a series object(like a list,just one column of the table)

#TODO 4:Convert dataframe to dict(refer to Pandas API reference)
# data_dict=data.to_dict()
# print(data_dict)

#TODO 5:Convert series to list
# data_list=data["temp"].to_list()
# print(data_list)

# TODO 6:Get Average temperature
# avg=sum(data_list)/len(data_list)
# print(avg)
# #OR
# print(data["temp"].mean())

#TODO 7:Get maximum temperature
# max_temp=(data["temp"].max())
# print(max_temp)

#TODO 8:Get data in a row example, for day Monday
# monday=(data[data.day=="Monday"])
# print(monday)

#TODO 9:Get row of data where temperature was max
# print(data[data.temp==max_temp])

#TODO 10:Print condition for Monday
# print(monday.condition)

#TODO 11:Get temp for Monday,convert to Fahrenheit
# monday_temp=int(monday.temp)
# fah=monday_temp*9/5+32
# print(fah)

#TODO 12:Create dataframe from scratch
data_dict={
    "students":["Amy","James","Angela"],
    "scores":[76,56,65]
}
data=pandas.DataFrame(data_dict)
print(data)
#lets convert this to new csv file that will get stored inside Day025 folder
data.to_csv("100 Days of Code - The Complete Python Pro Bootcamp for 2023/python files/Day 25/weather-data.csv")