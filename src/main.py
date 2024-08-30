# main.py
import fastapi
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy
from typing import List
from pydantic import BaseModel

# Incorrect imports (to be fixed by ast-grep)
import database
import schemas
import models
import crud
import auth

app = fastapi.FastAPI()

@app.post("/users", response_model=schemas.UserInDB)
def register_user(user: schemas.UserCreate, db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    db_user = crud.create_user(db, user)
    return schemas.UserInDB(id=db_user.id, username=db_user.username)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = fastapi.Depends(), db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/blog_posts", response_model=schemas.BlogPostInDB)
async def create_post(
    blog_post: schemas.BlogPostCreate,
    current_user: models.User = fastapi.Depends(auth.get_current_user),
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)
):
    return crud.create_blog_post(db, blog_post, current_user.id)

@app.get("/blog_posts", response_model=List[schemas.BlogPostInDB])
async def read_posts(skip: int = 0, limit: int = 10, db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    return crud.get_blog_posts(db, skip, limit)

@app.get("/blog_posts/{post_id}", response_model=schemas.BlogPostInDB)
async def read_post(post_id: int, db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    post = crud.get_blog_post(db, post_id)
    if post is None:
        raise fastapi.HTTPException(status_code=404, detail="Blog post not found")
    return post

@app.put("/blog_posts/{post_id}", response_model=schemas.BlogPostInDB)
async def update_post(
    post_id: int,
    blog_post: schemas.BlogPostUpdate,
    current_user: models.User = fastapi.Depends(auth.get_current_user),
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)
):
    updated_post = crud.update_blog_post(db, post_id, blog_post, current_user.id)
    if updated_post is None:
        raise fastapi.HTTPException(status_code=404, detail="Blog post not found")
    return updated_post

@app.delete("/blog_posts/{post_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: models.User = fastapi.Depends(auth.get_current_user),
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)
):
    success = crud.delete_blog_post(db, post_id, current_user.id)
    if not success:
        raise fastapi.HTTPException(status_code=404, detail="Blog post not found")
    return {"detail": "Blog post deleted successfully"}

@app.post("/blog_posts/{post_id}/comments", response_model=comments.CommentInDB)
async def add_comment(
    post_id: int,
    comment: comments.CommentCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)
):
    return comments.add_comment(db, comment, post_id)

@app.get("/blog_posts/{post_id}/comments", response_model=List[comments.CommentInDB])
async def get_post_comments(
    post_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)
):
    return comments.get_comments(db, post_id)

import fastapi.responses
@app.get("/health")
async def health_check():
    return fastapi.responses.JSONResponse(content={"status": "healthy"})


@app.post("/categories", response_model=CategoryCreate)
async def create_category(
    category: CategoryCreate,
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db),
    current_user: models.User = fastapi.Depends(auth.get_current_user)
):
    # Simulating category creation
    new_category = {
        "name": category.name,
        "description": category.description,
        "created_by": current_user.username
    }
    
    # Log category creation
    print(f"New category created: {new_category['name']}")
    
    return CategoryCreate(**new_category)