import streamlit as st
import pandas as pd
import json
from llm import generate_testcase



st.title("TestCases Generator Tool")

# Defining the sidebar content
with st.sidebar:
    st.title("About TestCase Generator!!!")
    st.title("_TestCase Generator_ is :blue[cool] :sunglasses:") 
    st.write("""A Test Case Generator is an automated tool designed to accelerate the software testing lifecycle by transforming requirements, 
    user stories, or application code into comprehensive, executable test cases. By leveraging algorithms or AI models, 
    these tools ensure broad test coverage while reducing the manual effort traditionally required to document edge cases and validation steps.""")


# requirement = "Create a 5 test cases for Web Login functionality.The test cases should cover the following scenarios: 1. Valid login with correct username and password.2. Invalid login with incorrect username. 3. Invalid login with incorrect password. 4. Empty username and password fields. 5. Account lockout after multiple failed login attempts. Publish the results in tabular format with the following columns: Test Case ID, Test Case Description, Expected Results. The test case IDs should be in the format TC001, TC002, etc."
requirement = st.chat_input("Enter the User Story / requirement")
with st.chat_message("ai", avatar=None):
    st.write("Hello 👋 Welcome to the TestCases Generator Tool!, Happy to help you generate test cases!")
if requirement:
    with st.chat_message("user", avatar=None):
        st.write(f"{requirement}")
    if requirement.strip():
        with st.spinner("Generating..."):
            result = generate_testcase(requirement)
            with st.chat_message("ai", avatar=None):
                st.write(result)
            
    else:
        st.warning("Please enter the requirements!!!")