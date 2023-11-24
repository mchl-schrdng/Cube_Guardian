import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

# Function to execute cube testing script
def job_function():
    subprocess.run(["python", "./services/cube_tester.py"], check=True)

# Initialize scheduler in session state
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = BackgroundScheduler()
    if not st.session_state.scheduler.running:
        st.session_state.scheduler.start()

# Page title
st.title('Advanced Cube Check Scheduler')
st.subheader('', divider='rainbow')

# Select schedule type
schedule_type = st.selectbox("Select schedule type", ['Interval', 'Daily', 'Weekly', 'Monthly'])

# Time selection initialization
hour = 0
minute = 0

# Options for Weekly and Monthly scheduling
if schedule_type == 'Weekly':
    day_of_week = st.selectbox("Select day of the week", ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
elif schedule_type == 'Monthly':
    day_of_month = st.slider("Select day of the month", min_value=1, max_value=31, value=1)

# Options for Interval scheduling
if schedule_type == 'Interval':
    interval_type = st.selectbox("Interval type", ['Minutes', 'Hours'])
    interval_value = st.number_input(f"Every (in {interval_type})", min_value=1, max_value=60, value=1)

# Time selection for Daily, Weekly, and Monthly schedules
if schedule_type in ['Daily', 'Weekly', 'Monthly']:
    hour = st.slider("Select hour for execution", 0, 23, 0)
    minute = st.slider("Select minute for execution", 0, 59, 0)

# Schedule job button
if st.button("Schedule Job"):
    job_kwargs = {'hour': hour, 'minute': minute}
    if schedule_type == 'Interval':
        if interval_type == 'Minutes':
            st.session_state.scheduler.add_job(job_function, 'interval', minutes=interval_value)
        else:
            st.session_state.scheduler.add_job(job_function, 'interval', hours=interval_value)
    elif schedule_type == 'Daily':
        st.session_state.scheduler.add_job(job_function, 'cron', **job_kwargs)
    elif schedule_type == 'Weekly':
        st.session_state.scheduler.add_job(job_function, 'cron', day_of_week=day_of_week.lower(), **job_kwargs)
    elif schedule_type == 'Monthly':
        st.session_state.scheduler.add_job(job_function, 'cron', day=day_of_month, **job_kwargs)
    st.success("Job scheduled successfully!")

# Display scheduled jobs
st.sidebar.image("./img/logo.png", width=350)
st.subheader('', divider='rainbow')
st.header("Scheduled Jobs")
col1_title, col2_title, col3_title = st.columns([2, 8, 2])
with col1_title:
    st.markdown("**Job ID**")
with col2_title:
    st.markdown("**Interval**")
with col3_title:
    st.markdown("**Action**")

for job in st.session_state.scheduler.get_jobs():
    col1, col2, col3 = st.columns([2, 8, 2])
    with col1:
        st.write(job.id)
    with col2:
        st.write(f"{job.trigger}")
    with col3:
        if st.button("Delete", key=job.id):
            st.session_state.scheduler.remove_job(job.id)
            st.rerun()