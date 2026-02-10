from pydantic import BaseModel
from typing import List

class TestCase(BaseModel):
    tcId:int
    tcDescription: str
    tSteps: str
    tExpectedResults: str
    
class TestCaseResponse(BaseModel):
    test_case: List[TestCase]