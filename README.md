import streamlit as st

st.set_page_config(
    page_title="Quality checks for Cube", 
    layout="wide",
    page_icon="./img/logo.png"
)

st.sidebar.subheader('', divider='rainbow')
st.sidebar.image("./img/logo.png", width=300)
st.sidebar.markdown("<h1 style='text-align: center;'>CubeGuardian</h1>", unsafe_allow_html=True)
st.sidebar.subheader('', divider='rainbow')
