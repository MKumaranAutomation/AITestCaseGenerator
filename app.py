import streamlit as st
from llm import generate_testcase



st.title("TestCases Generator Tool")
requirement =st.chat_input(
    "Enter the User Story / requirement"

)

requirement = " Create a 5 test cases for mobile app"

if st.button("Generate TestCases"):
    if requirement.strip():
        with st.spinner("Generating..."):
            result = generate_testcase(requirement)
        
        st.write(result)
        # for tc in result.test_case:
        #     st.subheader(f"{tc.tcId}")
        #     st.write(f"**TestCase Description: **{tc.tcDescription}")
        #     st.write(f"**Expected Results: **{tc.tExpectedResults}")
            
    else:
        st.warning("Please enter the requirements!!!")
            
            