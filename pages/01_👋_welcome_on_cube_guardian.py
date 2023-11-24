# CubeGuardianApp/pages/02_about_cube_guardian.py

import streamlit as st

def main():
    st.sidebar.image("./img/logo.png", width=350)

    st.title("Welcome to CubeGuardian")
    st.write("CubeGuardian is a comprehensive tool designed for CI/CD and quality checks in Cube.js applications...")

    st.subheader('', divider='rainbow')
    st.markdown("<h1 style='text-align: center;'>CubeGuardian</h1>", unsafe_allow_html=True)

    # Features of CubeGuardian
    st.header("Key Features")
    st.markdown("""
    - **Automated Quality Checks**: Run comprehensive tests on your Cube.js applications to ensure code quality and reliability.
    - **CI/CD Integration**: Seamlessly integrate with your existing CI/CD pipelines for efficient and automated deployment workflows.
    - **Real-time Monitoring and Alerts**: Stay informed about your application's health with real-time monitoring and instant alert notifications.
    - **Detailed Analytics and Reporting**: Gain insights into your application's performance with in-depth analytics and customizable reports.
    - **User-Friendly Interface**: Easy-to-use interface, allowing you to manage and monitor your Cube.js applications effortlessly.
    """)

    # How CubeGuardian Can Help
    st.header("How Can CubeGuardian Help You?")
    st.write("""
    Whether you're developing a new Cube.js application or maintaining an existing one, CubeGuardian helps streamline your workflow. 
    It ensures that every deployment meets the highest quality standards, reducing downtime and improving user experience. 
    With CubeGuardian, you can focus more on development and less on the intricacies of deployment and monitoring.
    """)

    # Getting Started with CubeGuardian
    st.header("Getting Started with CubeGuardian")
    st.write("To begin using CubeGuardian, navigate through the application using the menu. Here are some quick tips to get you started:")
    st.markdown("""
    - **Quality Checks**: Access the quality check dashboard to view recent test results and performance metrics.
    - **Analysis and Reporting**: Dive into detailed reports and analysis for in-depth understanding of your application's health.
    - **Configuration**: Customize CubeGuardian settings to fit your specific CI/CD and monitoring needs.
    - **Support and Documentation**: Access our comprehensive documentation and support resources for any assistance.
    """)

    # Footer
    st.subheader("Ready to enhance your Cube.js development?")
    st.write("CubeGuardian is here to assist you every step of the way. Start exploring the app now and take your Cube.js projects to the next level!")

if __name__ == "__main__":
    main()