"""
Models for JSON Placeholder API
"""

from pydantic import BaseModel


class Post(BaseModel):
    """
    Represents a post resource returned by the JSONPlaceholder API.
    To not be confused with the POST method, this class is named "Post" because it models a post resource,
    not an HTTP POST request. Same for the others below
    """

    userId: int
    id: int
    title: str
    body: str


class PostCreate(BaseModel):
    """
    Payload schema for creating a new post via http POST requests on /posts.
    """

    userId: int
    title: str
    body: str


class PostUpdate(BaseModel):
    """
    Payload schema for replacing a post via http PUT requests on /posts/{id}.
    """

    id: int
    userId: int
    title: str
    body: str
