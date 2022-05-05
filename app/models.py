from pydantic import BaseModel


class QuestionQuery(BaseModel):
    questions_num: int
