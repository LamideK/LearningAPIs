from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import psycopg
import psycopg_binary
from psycopg2.extras import RealDictCursor
import time
#from psycopg2.extras import RealDictCursor
#from psycopg_binary.extras import RealDictCursor



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #Optional field with default value
    #rating : Optional[int] = None #Optional field that defaults to none
    #user: str

#connect to the database // Also, try again with plain psycopg
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database= 'FASTAPI', user= 'postgres', password= 'User@123', cursor_factory= RealDictCursor)  #, cursor_factory= RealDictCursor
        cursor = conn.cursor()
        print('Successful')
        break
    except Exception as e:
        print('Error: ', e)
        time.sleep(4) #Best for testing against internet problems, not authentication


# for put method
#class PostUpdate(Post):
#    super(t, obj)

my_posts = [{"title": "title of post", "content": "content of post", "id":1}, {"title": "A random title", "content": "content of post again", "id":2}]

@app.get('/') # this is called a decorator
async def root():
    return {"message": "Hello LamBam"}

def find_post(id):
    for p in my_posts:
        if p['id'] == id: #comparing string and int won't work
            return p 

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



@app.get('/posts')
async def get_posts():
    cursor.execute("""Select * from posts""")
    posts = cursor.fetchall()
    print(posts)
    return{"data": posts}


@app.post('/newpost', status_code=status.HTTP_201_CREATED)
async def create_posts(new_post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) values (%s, %s, %s) RETURNING *""" , (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return{"data successfully added": post}


@app.get('/posts/{id}') #id is known as a path parameter here
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)) )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found")
    return{'post_detail': post}

# title str, content str

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
     #return{"message: ": "post successfully deleted"} #preferred
    return Response(status_code=status.HTTP_204_NO_CONTENT) #this is standard practice


@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = RETURNING *""", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    return{'data: ': updated_post}

""" @app.patch('/posts/{id}')
async def update_part_of_post(id: int, post: Post): """

