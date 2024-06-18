from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import models, schemas, utils, config
from database import engine, get_db
import routers
from routers import users, post, auth, vote


# Alembic handles this now
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com/"]
# for all domain, "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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



@app.exception_handler(ValidationError)
async def http_exception_handler(request, exc: ValidationError):
    errors = [{"field": err["loc"][0], "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"msg": "Validation Error", "dtails": errors},
    )


**Consider updating to show either method or API
@app.exception_handler(ValidationError)
async def http_exception_handler(request, exc: ValidationError):
    errors = [
        {
            "field": err["loc"][0],
            "message": err["msg"],
            # "input": err["input"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={"msg": "Validation Error", "dtails": errors},
    )



"""
