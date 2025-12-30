from pydantic import BaseModel



class QuestionModel(BaseModel):
    user : str
    question : str


