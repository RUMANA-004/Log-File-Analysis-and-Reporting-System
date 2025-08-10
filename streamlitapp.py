import streamlit as st
import mysql.connector
import pandas as pd

st.title("📊 Web Server Log Analyzer - Dashboard")

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Asrc$1122",
    database="weblogs_db"
)
cursor = conn.cursor()

# Sidebar - Report Selection
option = st.sidebar.selectbox(
    "Select Report",
    ["Top N IPs", "Status Code Distribution", "Hourly Traffic"]
)

if option == "Top N IPs":
    n = st.sidebar.number_input("Enter N", min_value=1, max_value=50, value=5)
    query = f"""
        SELECT ip_address, COUNT(*) AS request_count
        FROM log_entries
        GROUP BY ip_address
        ORDER BY request_count DESC
        LIMIT {n}
    """
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["IP Address", "Request Count"])
    st.dataframe(df)

elif option == "Status Code Distribution":
    query = """
        SELECT status_code, COUNT(*) AS count
        FROM log_entries
        GROUP BY status_code
    """
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Status Code", "Count"])
    st.bar_chart(df.set_index("Status Code"))

elif option == "Hourly Traffic":
    query = """
        SELECT HOUR(timestamp) AS hour, COUNT(*) AS request_count
        FROM log_entries
        GROUP BY hour
        ORDER BY hour
    """
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["Hour", "Request Count"])
    st.line_chart(df.set_index("Hour"))

cursor.close()
conn.close()
