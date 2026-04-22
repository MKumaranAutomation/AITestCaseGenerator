import re

from langchain_ollama import OllamaLLM
from schemas import TestCaseResponse
from prompts import SYSTEM_PROMPT, USER_PROMPT
import pandas as pd
from pandas import json_normalize
import json

llm = OllamaLLM(
    model = "mistral",
    temperature = 0.2
)

def generate_testcase(requirement: str, history: list = None):
    # Format chat history for the prompt
    history_str = ""
    if history:
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            if isinstance(content, pd.DataFrame):
                content = "Generated a test case table."
            history_str += f"{role}: {content}\n"

    prompt = SYSTEM_PROMPT + USER_PROMPT.format(
        requirement=requirement,
        history=history_str
    )

    raw_response = llm.invoke(prompt)

    # Clean up markdown artifacts
    clean_content = re.sub(r"```json|```", "", raw_response).strip()
    
    # Check if the response is likely JSON
    has_json = '{' in clean_content and '}' in clean_content
    
    if has_json:
        try:
            # Find JSON boundaries
            start_obj = clean_content.find('{')
            end_obj = clean_content.rfind('}') + 1
            start_list = clean_content.find('[')
            end_list = clean_content.rfind(']') + 1

            data = None
            if start_obj != -1 and (start_list == -1 or start_obj < start_list):
                data = json.loads(clean_content[start_obj:end_obj])
            elif start_list != -1:
                data = json.loads(clean_content[start_list:end_list])

            if data:
                # Handle various nested structures
                test_cases = []
                if isinstance(data, dict):
                    if "test_cases" in data:
                        test_cases = data["test_cases"]
                    elif all(isinstance(v, dict) for v in data.values()):
                        for v in data.values():
                            if "properties" in v:
                                test_cases.append(v["properties"])
                            else:
                                test_cases.append(v)
                    else:
                        test_cases = [data]
                elif isinstance(data, list):
                    test_cases = data

                # Convert to DataFrame
                df = pd.DataFrame(test_cases)
                
                if not df.empty:
                    # Human readable formatting for steps
                    if 'tSteps' in df.columns:
                        df['tSteps'] = df['tSteps'].apply(
                            lambda x: "\n".join([str(i+1) + ". " + str(s) for i, s in enumerate(x)]) 
                            if isinstance(x, list) else str(x)
                        )
                    
                    # Reorder columns
                    desired_order = ['tcId', 'tcDescription', 'priority', 'preConditions', 'tSteps', 'tExpectedResults']
                    current_cols = [c for c in desired_order if c in df.columns]
                    df = df[current_cols]

                return df
        except Exception as e:
            # If JSON parsing fails, treat it as a text response
            print(f"JSON Parsing failed: {e}")
            return raw_response

    # If no JSON or parsing failed, return the raw text
    return raw_response