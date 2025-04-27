from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class ChoiceBase(BaseModel):
    """Base model for quiz choices."""
    choice_text: str = Field(default="", description="The text of the choice")
    is_correct: bool = Field(default=False, description="Indicates if this is the correct answer")

class QuestionBase(BaseModel):
    """Base model for quiz questions."""
    question_text: str = Field(default="", description="The text of the question")
    choices: List[ChoiceBase] = Field(default_factory=list, description="List of possible answers")

    class Config:
        json_schema_extra = {
            "example": {
                "question_text": "Quelle est la capitale de la France?",
                "choices": [
                    {"choice_text": "Paris", "is_correct": True},
                    {"choice_text": "Lyon", "is_correct": False},
                    {"choice_text": "Marseille", "is_correct": False}
                ]
            }
        }


@app.post("/questions/")
def create_question(question: QuestionBase):
    return {"message": "Question reçue !", "data": question}
