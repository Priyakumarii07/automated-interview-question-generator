from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    type: str
    question: str
    options: Optional[List[str]] = []
    answer: str
    explanation: str

class QuestionResponse(BaseModel):
    questions: List[Question]