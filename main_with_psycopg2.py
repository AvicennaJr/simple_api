from fastapi import FastAPI, Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class  Post(BaseModel):
    title: str
    content: str
    published: bool = True

#Create a database with postgresql and connect it with psycopg2. Make sure the database is online.

while True:
  try:
      conn = psycopg2.connect(
          host='localhost',
          user='postgres',
          password='password',
          database='fastapi_tutorial', 
          cursor_factory=RealDictCursor
      )
      cursor = conn.cursor()
      print("Connection to database successful")
  except:
      print('Something went wrong')
      time.sleep(5)

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ",
    (post.title, post.content, post.published))
    new_post = cursor.fetchone() #returns what we get above
    conn.commit() #make changes in the database
    return {"data": new_post} 

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * from posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} was not found")
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING * ", (str(id),))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} was not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    ( post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} was not found")
    
    return {"message": updated_post}
