import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Function to fetch results from a specific table
def fetch_results(table_name):
    conn = sqlite3.connect('services/db/tables/cube_test_results.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    df = pd.DataFrame(results, columns=column_names)
    conn.close()
    return df

# Function to calculate pass and fail rates
def calculate_pass_fail_rate(df):
    passed = df[df['status'] == 'passed'].shape[0]
    failed = df[df['status'] == 'failed'].shape[0]
    total = passed + failed
    pass_rate = (passed / total) * 100 if total > 0 else 0
    fail_rate = (failed / total) * 100 if total > 0 else 0
    return pass_rate, fail_rate

# Function to calculate pass/fail rate for each cube, formatted as percentages
def calculate_cube_pass_fail_rate(df):
    cube_rates = df.groupby('cube_name')['status'].apply(lambda x: x.value_counts(normalize=True)).unstack().fillna(0)
    cube_rates = cube_rates.rename(columns={'passed': 'Passed Rate', 'failed': 'Fail Rate'})
    cube_rates['Passed Rate'] = cube_rates['Passed Rate'].apply(lambda x: f"{x * 100:.2f}%")
    cube_rates['Fail Rate'] = cube_rates['Fail Rate'].apply(lambda x: f"{x * 100:.2f}%")
    cube_rates = cube_rates[['Passed Rate', 'Fail Rate']]  # Reorder columns if needed
    return cube_rates

# Function to create a stacked bar graph for daily checks
def create_stacked_bar_chart(df):
    df['date'] = pd.to_datetime(df['date']).dt.date
    df_grouped = df.groupby(['date', 'status']).size().reset_index(name='count')
    fig = px.bar(df_grouped, x='date', y='count', color='status', title='Daily Checks (Passed in Green, Failed in Red)')
    fig.update_xaxes(dtick="D1", tickformat="%Y-%m-%d")  # Update to show only days
    return fig

# Streamlit App Layout
st.sidebar.image("./img/logo.png", width=350)
st.title('Quality Analysis Dashboard')

# KPI 1: Overall Pass/Fail Rate in Table (Overall Status)
st.subheader('KPI 1: Overall Pass/Fail Rate')
df_overall = fetch_results('overall_status')
pass_rate, fail_rate = calculate_pass_fail_rate(df_overall)
overall_rates = pd.DataFrame({'Pass Rate': [f"{pass_rate:.2f}%"], 'Fail Rate': [f"{fail_rate:.2f}%"]})
bar_chart = create_stacked_bar_chart(df_overall)
st.table(overall_rates)

st.plotly_chart(bar_chart)

# KPI 2: Pass/Fail Rate by Cube in Table (Cube Status)
st.subheader('KPI 2: Pass/Fail Rate by Cube')
df_cube_status = fetch_results('cube_status')
cube_rates = calculate_cube_pass_fail_rate(df_cube_status)
st.table(cube_rates)

# Placeholder for additional KPIs
st.subheader('More KPIs')
st.write("Additional KPIs can be added here, such as Test Coverage, Error Type Distribution, Time to Fix, etc., based on available data.")

# Footer
st.write("Note: The specific KPIs and their implementations will depend on the available data and the specific goals of your quality analysis.")