import streamlit as st
import psycopg2
import pandas as pd

# db connection
def get_connection():
    return psycopg2.connect(host='localhost',database='Redbus',user='postgres',password='1234')

# dropdown for routes
def fetch_route_names(connection):
    query = "SELECT DISTINCT route_name FROM bus_routes ORDER BY route_name"
    route_names = pd.read_sql(query, connection)['route_name'].tolist()
    return route_names

# filters
def fetch_filtered_data(connection, route_name, price_sort_order, star_ratings, bus_types):
    price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
    
    query = f"""
    SELECT * FROM bus_routes 
    WHERE route_name = %s
    """
    # filters for bus rating and types
    if star_ratings:
        query += f" AND star_rating IN ({', '.join(['%s'] * len(star_ratings))})"
    if bus_types:
        query += f" AND bus_type IN ({', '.join(['%s'] * len(bus_types))})"
    
    query += f" ORDER BY star_rating DESC, price {price_sort_order_sql}"
    params = [route_name] + star_ratings + bus_types
    data = pd.read_sql(query, connection, params=params)
    return data

# streamlit application
def main():
    st.title('Bus Tickets Booking Dashboard')
    connection = get_connection()

    try:
        st.sidebar.header('Filter Options')
        route_names = fetch_route_names(connection)
        selected_route = st.sidebar.selectbox('Select Route Name', route_names)
        price_sort_order = st.sidebar.selectbox('Sort by Price', ['Low to High', 'High to Low'])

        if selected_route:
            data = fetch_filtered_data(connection, selected_route, price_sort_order, [], [])

            if not data.empty:
                star_ratings = data['star_rating'].unique().tolist()
                selected_ratings = st.sidebar.multiselect('Filter by Star Rating', star_ratings)
                bus_types = data['bus_type'].unique().tolist()
                selected_bus_types = st.sidebar.multiselect('Filter by Bus Type', bus_types)
                filtered_data = fetch_filtered_data(connection, selected_route, price_sort_order, selected_ratings, selected_bus_types)

                if not filtered_data.empty:
                    st.write(f"### Bus Data for Route: {selected_route}")
                    st.dataframe(filtered_data)
                else:
                    st.write("No data available for the selected filters.")
            else:
                st.write(f"No data found for the route: {selected_route}.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
