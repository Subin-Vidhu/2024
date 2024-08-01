import pandas as pd

# Create a DataFrame with the dummy data
data = {
    'Date': ['Jul 28, 2024', 'Jul 28, 2024', 'Jul 28, 2024', 'Jul 28, 2024',
             'Jul 28, 2024', 'Jul 28, 2024', 'Jul 29, 2024', 'Jul 29, 2024',
             'Jul 29, 2024', 'Jul 29, 2024', 'Jul 29, 2024', 'Jul 29, 2024'],
    'Time': ['08:00:00 AM', '01:00:00 PM', '02:00:00 PM', '05:00:00 PM',
             '09:00:00 AM', '06:00:00 PM', '09:00:00 AM', '11:00:00 AM',
             '12:00:00 PM', '04:00:00 PM', '09:00:00 AM', '04:00:00 PM'],
    'Name': ['Alice', 'Alice', 'Alice', 'Alice',
             'Bob', 'Bob', 'Alice', 'Alice',
             'Alice', 'Alice', 'Bob', 'Bob'],
    'Direction': ['entry', 'exit', 'entry', 'exit',
                  'entry', 'exit', 'entry', 'exit',
                  'entry', 'exit', 'entry', 'exit']
}

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
file_path = r'c:\Users\Subin-PC\Downloads/Dummy_Access_History.xlsx'
df.to_excel(file_path, index=False, sheet_name='Access History')

