import streamlit as st
import pandas as pd
import json
from llm import generate_testcase
import pypdf
import docx
import io

def extract_text_from_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel", "text/csv"]:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            return df.to_string()
    except Exception as e:
        st.error(f"Error parsing file: {e}")
    return None

st.set_page_config(page_title="AI Test Case Generator", page_icon="🧪", layout="wide")
st.title("TestCases Generator Tool")

# Defining the sidebar content
with st.sidebar:
    st.title("About TestCase Generator!!!")
    st.title("_TestCase Generator_ is :blue[cool] :sunglasses:") 
    st.write("""A Test Case Generator is an automated tool designed to accelerate the software testing lifecycle by transforming requirements, 
    user stories, or application code into comprehensive, executable test cases. By leveraging algorithms or AI models, 
    these tools ensure broad test coverage while reducing the manual effort traditionally required to document edge cases and validation steps.""")
    
    st.divider()
    st.subheader("📁 Upload Requirements")
    uploaded_file = st.file_uploader("Upload Doc, Excel, or PDF", type=["pdf", "docx", "xlsx", "xls", "csv"])
    if uploaded_file:
        with st.spinner("Extracting text from file..."):
            file_text = extract_text_from_file(uploaded_file)
            if file_text:
                st.success("File content extracted!")
                st.session_state.file_content = file_text
            else:
                st.error("Failed to extract text from file.")



# requirement = "Create a 5 test cases for Web Login functionality.The test cases should cover the following scenarios: 1. Valid login with correct username and password.2. Invalid login with incorrect username. 3. Invalid login with incorrect password. 4. Empty username and password fields. 5. Account lockout after multiple failed login attempts. Publish the results in tabular format with the following columns: Test Case ID, Test Case Description, Expected Results. The test case IDs should be in the format TC001, TC002, etc."
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hello 👋 I'm your Senior QA Engineer assistant. I can help you generate comprehensive test cases or answer any questions about the QA process. How can I help you today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], pd.DataFrame):
            st.dataframe(message["content"], use_container_width=True)
        else:
            st.markdown(message["content"])

# Chat input
requirement = st.chat_input("Enter your requirement or ask a question...")

if requirement:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": requirement})
    with st.chat_message("user"):
        st.markdown(requirement)

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            # If a file was uploaded, combine its content with the user's requirement
            final_requirement = requirement
            if "file_content" in st.session_state and st.session_state.file_content:
                final_requirement = f"REQ_FROM_FILE:\n{st.session_state.file_content}\n\nUSER_REQUEST:\n{requirement}"

            # Pass full history to generate_testcase
            result = generate_testcase(final_requirement, history=st.session_state.messages[:-1])
            
            if isinstance(result, pd.DataFrame):
                if not result.empty:
                    st.success("Test cases generated successfully!")
                    st.dataframe(result, use_container_width=True)
                    st.session_state.messages.append({"role": "ai", "content": result})
                else:
                    st.error("I couldn't generate test cases for that. Could you provide more details?")
            else:
                # Regular text response
                st.markdown(result)
                st.session_state.messages.append({"role": "ai", "content": result})