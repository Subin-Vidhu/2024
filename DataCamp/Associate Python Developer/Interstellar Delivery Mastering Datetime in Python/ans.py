from datetime import datetime, timedelta

# Define format_date function accepting timestamp and datetime format args
def format_date(timestamp, datetime_format):
    # Convert timestamp arg to datetime object and save result in new variable
    datetime_obj = datetime.fromtimestamp(timestamp)  
    # Format datetime_obj to string using the datetime_format arg
    datetime_str = datetime_obj.strftime(datetime_format)
    # Return formatted datetime string
    return datetime_str

# Define calculate_landing_time function accepting launch datetime and duration
def calculate_landing_time(rocket_launch_dt, travel_duration):
    # Calculate landing by adding travel_duration to rocket_launch_dt arg and save result in new variable
    landing_date = rocket_launch_dt + timedelta(days=travel_duration)
    # Format landing datetime to string in specified format
    landing_date_string = landing_date.strftime("%d-%m-%Y") 
    # Return landing date time string 
    return landing_date_string

# Define days_until_delivery function accepting expected and current datetimes 
def days_until_delivery(expected_delivery_dt, current_dt):
    # Calculate the time until delivery by subtracting current_dt arg from the expected_delivery_dt arg 
    time_until_delivery = expected_delivery_dt - current_dt
    # Access the date component of the datetime object
    days_until = time_until_delivery.days
    # Return number of days until delivery
    return days_until