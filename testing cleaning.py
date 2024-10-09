import pandas as pd
import re


def extract_seat_number(val):
    if isinstance(val, str):
        num_str = re.findall(r'\d+', val)
        if num_str:
            return int(''.join(num_str))  
    elif isinstance(val, (int, float)):
        return int(val)
    return 0  

df = pd.read_csv('bus_route.csv') 

if 'Seat_Availability' in df.columns:
    df['Seat_Availability'] = df['Seat_Availability'].apply(extract_seat_number)

df.to_csv('cleaned_csv_file.csv', index=False)  


print(df.head())
