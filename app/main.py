from fastapi import FastAPI
import models, schemas, utils, config
from database import engine, get_db
import routers
from routers import users, post, auth, vote


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")  # this is called a decorator
async def root():
    return {"message": "Hello..."}


"""connect to the database // Also, try again with plain psycopg
from psycopg2.extras import RealDictCursor
from psycopg_binary.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'FASTAPI', user= 'postgres', password= 'Post123', cursor_factory= RealDictCursor)  #, cursor_factory= RealDictCursor
        cursor = conn.cursor()
        print('Successful')
        break
    except Exception as e:
        print('Error: ', e)
        time.sleep(4) #Best for testing against internet problems, not authentication
"""
