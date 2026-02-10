import streamlit as st
from llm import generate_testcase

st.set_page_config(page_title="TestCases Generator Tool")

st.title("TestCases Generator Tool")

requirement = st.text_area(
    "Enter the User Story / requirement",
    height= 150
)

if st.button("Generate TestCases"):
    if requirement.strip():
        with st.spinner("Generating..."):
            result = generate_testcase(requirement)
        
        for tc in result.test_case:
            st.subheader(f"{tc.tcId}")
            st.write(f"**TestCase Description: **{tc.tcDescription}")
            st.write(f"**Expected Results: **{tc.tExpectedResults}")
            
    else:
        st.warning("Please enter the requirements!!!")
            
            