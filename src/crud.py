# crud.py
from sqlalchemy.orm import Session
from models import User, BlogPost
from schemas import UserCreate, BlogPostCreate, BlogPostUpdate
from auth import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_blog_post(db: Session, blog_post: BlogPostCreate, author_id: int):
    db_post = BlogPost(title=blog_post.title, content=blog_post.content, author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_blog_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(BlogPost).offset(skip).limit(limit).all()

def get_blog_post(db: Session, post_id: int):
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()

def update_blog_post(db: Session, post_id: int, blog_post: BlogPostUpdate, author_id: int):
    db_post = db.query(BlogPost).filter(BlogPost.id == post_id, BlogPost.author_id == author_id).first()
    if db_post is None:
        return None
    
    if blog_post.title:
        db_post.title = blog_post.title
    if blog_post.content:
        db_post.content = blog_post.content
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_blog_post(db: Session, post_id: int, author_id: int):
    db_post = db.query(BlogPost).filter(BlogPost.id == post_id, BlogPost.author_id == author_id).first()
    if db_post is None:
        return False
    
    db.delete(db_post)
    db.commit()
    return True