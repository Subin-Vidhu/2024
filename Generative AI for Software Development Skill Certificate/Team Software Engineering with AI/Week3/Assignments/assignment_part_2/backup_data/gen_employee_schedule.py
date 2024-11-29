from internal_stats import *
from df_converter import *

df = parse_json_schedule_and_save('info.json')

tuples = []
for i in df.index:
    tuples.append(tuple(df.loc[i,['work_day_of_week', 'user_id']]))


if __name__ == "__main__":
    get_working_days_and_average_income(tuples)
    print("Files data.csv and info.json generated")






