from langchain_ollama import OllamaLLM
from schemas import TestCaseResponse
from prompts import SYSTEM_PROMPT, USER_PROMPT
import json

llm = OllamaLLM(
    model = "mistral",
    temperature = 0.2
)

def generate_testcase(requirement: str) -> TestCaseResponse:
    schema = json.dumps(TestCaseResponse.model_json_schema(), indent=2)

    prompt = SYSTEM_PROMPT + USER_PROMPT.format(
        requirement=requirement,
        schema=schema
    )

    raw_response = llm.invoke(prompt)

    clean_json = extract_json(raw_response)

    return TestCaseResponse.model_validate_json(clean_json)


def extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in LLM response")

    return text[start:end]


generate_testcase("Create a test case for login page")