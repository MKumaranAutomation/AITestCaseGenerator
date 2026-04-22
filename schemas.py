from pydantic import BaseModel
from typing import List

class TestCase(BaseModel):
    tcId: str
    tcDescription: str
    priority: str  # High, Medium, Low
    preConditions: str
    tSteps: List[str]
    tExpectedResults: str
    
class TestCaseResponse(BaseModel):
    test_cases: List[TestCase]