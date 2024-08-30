# main.py
import fastapi
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy
from typing import List
from pydantic import BaseModel

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

@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"deleted": item_id}

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


@app.get("/posts/{post_id}/analytics", response_model=PostAnalytics)
async def get_post_analytics(
    post_id: int,
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db),
    current_user: models.User = fastapi.Depends(auth.get_current_user)
):
    # Simulating fetching analytics data
    # In a real application, you would query this from a database
    analytics_data = {
        "post_id": post_id,
        "views": 1000,
        "likes": 50,
        "comments": 25,
        "last_viewed": datetime.datetime.now()
    }
    
    # Log analytics request
    print(f"Analytics requested for post {post_id} by user {current_user.username}")
    
    return PostAnalytics(**analytics_data)

# New endpoint to get analytics for all posts
@app.get("/posts/analytics", response_model=List[PostAnalytics])
async def get_all_posts_analytics(
    db: sqlalchemy.orm.Session = fastapi.Depends(database.get_db),
    current_user: models.User = fastapi.Depends(auth.get_current_user)
):
    # Simulating fetching analytics data for multiple posts
    analytics_data = [
        {
            "post_id": i,
            "views": 1000 * i,
            "likes": 50 * i,
            "comments": 25 * i,
            "last_viewed": datetime.datetime.now() - datetime.timedelta(days=i)
        }
        for i in range(1, 6)  # Simulating data for 5 posts
    ]
    
    # Log analytics request
    print(f"Analytics requested for all posts by user {current_user.username}")
    
    return [PostAnalytics(**data) for data in analytics_data]