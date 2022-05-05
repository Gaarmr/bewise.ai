from datetime import datetime
from fastapi import FastAPI
from app.db import database, Questions 
from app.models import QuestionQuery
import httpx


app = FastAPI(title="FastAPI, Docker")


@app.get("/")
async def read_root():
    result = await Questions.objects.all()
    print(len(result))
    return result


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    # await Questions.objects.get_or_create(question="Было три козла, сколько?", answer='Три', created_at=datetime.now())


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.post("/get_question/")
async def get_question(query: QuestionQuery):
    async with httpx.AsyncClient() as client:
        questions_to_create=[]
        while query.questions_num:
            r = await client.get(url='https://jservice.io/api/random', params={'count': query.questions_num})
            questions = r.json()
            questions_ids = [question['id'] for question in questions]
            existing_questions_ids = set(await Questions.objects.filter(id__in=questions_ids).values_list('id', flatten=True))
            for question in questions:
                if question['id'] in existing_questions_ids:
                    continue
                questions_to_create.append(
                    Questions(
                        id=question['id'], 
                        question=question['question'], 
                        answer=question['answer'], 
                        created_at=datetime.fromisoformat(question['created_at'].replace('Z',''))
                    )
                )
                existing_questions_ids.add(question['id'])
                query.questions_num -= 1

        await Questions.objects.bulk_create(questions_to_create)
        return questions_to_create

    # await Questions.objects.get_or_create(question="Было два козла, сколько?", answer='Два', created_at='Севодня')
    # return await Questions.objects.fields('id')
