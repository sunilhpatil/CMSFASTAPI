# Import libarires
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


# Base model
class Post (BaseModel):
    title : str
    content : str
    published : bool = True
    
#database connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database ='fastapi', user = 'postgres', password = 'admin',
        cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Databse connected")
        break
    except Exception as error:
        print("Database not connected")
        print("Error was :", error)
        time.sleep(5)


#test Data
my_posts = [
    {"title":"title 1", "content":"content1", "id":1},
    {"title":"title 2", "content":"content2", "id":2},
]

#find post
def find_post(id:int):
    for p in my_posts:
        if p["id"]== id:
            return p

#find index of post
def find_index(id:int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        

# root function
@app.get("/")
async def root():
    return {"message": "Hello FASTAPI"}


#get posts
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"post":posts}

#get single post
@app.get("/posts/{id}")
def get_post(id:int):

    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return {"post detail": post}

# create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
   ( post.title, post.content, post.published))

    new_post = cursor.fetchone()
    conn.commit()

    return {"Data": new_post}


# delete post
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post:Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""" , (post.title, post.content, (str(id),)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return{"data": updated_post}