from pydantic import BaseModel
from typing import List

class TestCase(BaseModel):
    tcId: str
    tcDescription: str
    tSteps: List[str]
    tExpectedResults: str
    
class TestCaseResponse(BaseModel):
    test_cases: List[TestCase]