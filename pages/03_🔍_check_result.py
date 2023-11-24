import pandas as pd
import sqlite3
import streamlit as st

# Function to execute a custom SQL query
def execute_query(query):
    conn = sqlite3.connect('services/db/tables/cube_test_results.db')
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

# Function to fetch results from a specific table, sorted by date and limited by the specified number of rows
def fetch_results(table_name, limit=None):
    conn = sqlite3.connect('services/db/tables/cube_test_results.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name} ORDER BY date DESC"
    if limit:
        query += f" LIMIT {limit}"
    cursor.execute(query)
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    df = pd.DataFrame(results, columns=column_names)
    conn.close()
    return df

# Function to generate an HTML table with custom styling based on the status
def generate_html_table(df, highlight_column):
    styles = {
        "failed": "background-color: rgba(255, 0, 0, 0.5); color: white;",  # Semi-transparent red
        "passed": "background-color: rgba(0, 128, 0, 0.5); color: white;"   # Semi-transparent green
    }
    table_html = "<table>"
    table_html += "<tr>" + "".join([f"<th>{col}</th>" for col in df.columns]) + "</tr>"
    for _, row in df.iterrows():
        style = styles.get(row[highlight_column].lower(), "")
        row_html = "<tr style='{}'>".format(style) + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
        table_html += row_html
    table_html += "</table>"
    return table_html

# Function to clear a specific table
def clear_table(table_name):
    conn = sqlite3.connect('services/db/tables/cube_test_results.db')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table_name}')
    conn.commit()
    conn.close()

# Function to create a table with a toggle for the number of displayed rows
def create_table_with_toggle(column, table_name, highlight_column):
    show_all = st.session_state.get(f'show_all_{table_name}', False)
    toggle_label = "Show All" if not show_all else "Show Less"
    if column.button(toggle_label, key=f'toggle_{table_name}'):
        st.session_state[f'show_all_{table_name}'] = not show_all

    limit = None if show_all else 10  # Change 10 to your preferred default number of rows
    df = fetch_results(table_name, limit)
    column.markdown(generate_html_table(df, highlight_column), unsafe_allow_html=True)

# Streamlit page setup
st.sidebar.image("./img/logo.png", width=350)
st.title('Cube Check Results')

# Custom SQL Query Section
st.subheader("Run Custom SQL Query")
query = st.text_area("Enter your SQL query here:", 
                     value="SELECT * FROM overall_status ORDER BY date DESC LIMIT 25",
                     height=150)
if st.button("Run Query"):
    result = execute_query(query)
    if isinstance(result, pd.DataFrame):
        st.write(result)
    else:
        st.error(result)

# Button to clear the tables
if st.button('Clear All Tables'):
    clear_table('overall_status')
    clear_table('cube_status')
    clear_table('dimension_status')
    st.success('Tables cleared successfully.')

# Displaying tables with toggle functionality
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Overall Status")
    create_table_with_toggle(col1, 'overall_status', "status")

with col2:
    st.header("Cube Status")
    create_table_with_toggle(col2, 'cube_status', "status")

with col3:
    st.header("Dimension Status")
    create_table_with_toggle(col3, 'dimension_status', "status")