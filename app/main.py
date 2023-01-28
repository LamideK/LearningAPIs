from fastapi import FastAPI
from . import models, schemas, utils
from .database import engine, get_db
from .utils import hash
from .routers import users, post

#from psycopg2.extras import RealDictCursor
#from psycopg_binary.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(users.router)

'''
#connect to the database 
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user= 'postgres', password= 'passw0rd', cursor_factory= RealDictCursor)  #, cursor_factory= RealDictCursor
        cursor = conn.cursor()
        print('Successful')
        break
    except Exception as e:
        print('Error: ', e)
        time.sleep(4) #Best for testing against internet problems, not authentication
'''

@app.get('/') # this is called a decorator  
async def root():
    return {"message": "Hello..."}


