import pandas as pd
import psycopg2
import re

csv_files = ["APSRTC_bus_details.csv","KSRTC_bus_details.csv","TSRTC_bus_details.csv",
             "KTCL_bus_details.csv","RSRTC_bus_details.csv","SBSTC_bus_details.csv",
             "HRTC_bus_details.csv","ASTC_bus_details.csv","UPSRTC_bus_details.csv","WBTC_bus_details.csv"]

df_list = [pd.read_csv(file) for file in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

combined_df.to_csv("bus_route.csv", index=False)
#to extract number from seat availability
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

# db connection
try:
    connection = psycopg2.connect(host='localhost',database='Redbus',user='postgres',password='1234')

    print("PostgreSQL connection established successfully.")

    table_name = "bus_routes"
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()

    # table for bus routes
    create_table_query = """
    CREATE TABLE IF NOT EXISTS bus_routes (
        id SERIAL PRIMARY KEY,
        route_name TEXT,
        route_link TEXT,
        bus_name TEXT,
        bus_type TEXT,
        departing_time TIME,
        duration TEXT,
        reaching_time TIME,
        star_rating FLOAT,
        price DECIMAL,
        seats_available INT
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
        connection.commit()
    print(f"Table '{table_name}' created successfully.")

    insert_query = f"""
    INSERT INTO {table_name} (route_name, route_link, bus_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seats_available) 
    VALUES %s
    """
    with connection.cursor() as cursor:
        for row in df.itertuples(index=False):
            cursor.execute(insert_query, (tuple(row),))
        connection.commit()
    print("Data inserted successfully into the bus_routes table.")

except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()
        print("PostgreSQL connection closed.")
        df.to_csv('bus_routes.csv', index=False) 


