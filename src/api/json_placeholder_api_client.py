"""
HTTP client for JSON Placeholder REST API.
"""

import logging

import requests

logger = logging.getLogger(__name__)


class JSONPlaceholderClient:
    """
    Client for interacting with the JSON Placeholder REST API
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        logger.info(f"Initialized JSONPlaceholderClient with base_url={self.base_url}")

    def _log_response(self, response: requests.Response) -> None:
        """
        Log the HTTP method, URL and status code of a response.
        """
        logger.info(f"{response.request.method} {response.request.url} → {response.status_code}")

    def get_posts(self) -> requests.Response:
        """
        GET /posts — retrieve all posts.
        """
        logger.debug("Fetching all posts")
        response = self.session.get(f"{self.base_url}/posts")
        self._log_response(response)
        return response

    def get_post(self, post_id: int) -> requests.Response:
        """
        GET /posts/{id} — retrieve a single post by ID.
        """
        logger.debug(f"Fetching post id={post_id}")
        response = self.session.get(f"{self.base_url}/posts/{post_id}")
        self._log_response(response)
        return response

    def create_post(self, payload: dict) -> requests.Response:
        """
        POST /posts — create a new post.
        """
        logger.debug(f"Creating post with payload={payload}")
        response = self.session.post(f"{self.base_url}/posts", json=payload)
        self._log_response(response)
        return response

    def update_post(self, post_id: int, payload: dict) -> requests.Response:
        """
        PUT /posts/{id} — update an existing post.
        """
        logger.debug(f"Updating post id={post_id} with payload={payload}")
        response = self.session.put(f"{self.base_url}/posts/{post_id}", json=payload)
        self._log_response(response)
        return response

    def delete_post(self, post_id: int) -> requests.Response:
        """
        DELETE /posts/{id} — delete a post.
        """
        logger.debug(f"Deleting post id={post_id}")
        response = self.session.delete(f"{self.base_url}/posts/{post_id}")
        self._log_response(response)
        return response

    def get_posts_by_user(self, user_id: int) -> requests.Response:
        """
        GET /posts?userId={id} — retrieve posts filtered by user ID.
        """
        logger.debug(f"Fetching posts for userId={user_id}")
        response = self.session.get(f"{self.base_url}/posts", params={"userId": user_id})
        self._log_response(response)
        return response
