import numpy as np
import json

def get_working_days_and_average_income(l):
    ''' 
    Given a list in the form [(day_1, user_1), (day_2, user_2), (day_3, user_3), ..., (day_n, user_n)]
    where day_i is a day of the week and user_i is a user_id (may be repeated), 
    returns a dictionary with the unique days appearing in the list and the users associated
    
    Example: [(Monday, a), (Tuesday, a), (Monday, b)]
    
    Returns: {a: [Monday, Tuesday], b: [Monday]}
    '''
    unique_values = np.unique(l, axis=0)
    dic = {}
    for day, user in unique_values:
        if user not in dic.keys():
            dic[user] = {"schedule": set([day])}
        else:
            dic[user]['schedule'].add(day)
    for key in dic.keys():
        dic[key]['schedule'] = list(dic[key]['schedule'])
        
    with open("schedule.json", 'w') as f:
        json.dump(dic, f)
