# FastAPI Blog API

This project is a simple blog API built with FastAPI, demonstrating basic CRUD operations, user authentication, and database integration.

## Project Structure

- `main.py`: The main FastAPI application
- `models.py`: SQLAlchemy ORM models
- `schemas.py`: Pydantic models for request/response validation
- `database.py`: Database connection and session management
- `auth.py`: Authentication and security functions
- `crud.py`: CRUD operations for the database
- `requirements.txt`: List of project dependencies

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fastapi-blog-api.git
   cd fastapi-blog-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

- POST `/users`: Create a new user
- POST `/token`: Login and get an access token
- POST `/blog_posts`: Create a new blog post (requires authentication)
- GET `/blog_posts`: Get a list of blog posts
- GET `/blog_posts/{post_id}`: Get a specific blog post
- PUT `/blog_posts/{post_id}`: Update a blog post (requires authentication)
- DELETE `/blog_posts/{post_id}`: Delete a blog post (requires authentication)

## Features

- User registration and authentication using JWT tokens
- CRUD operations for blog posts
- SQLite database integration using SQLAlchemy
- Pydantic models for request/response validation
- Interactive API documentation with Swagger UI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
