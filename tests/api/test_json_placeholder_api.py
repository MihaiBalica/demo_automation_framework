"""API tests for JSONPlaceholder (https://jsonplaceholder.typicode.com/)."""

import allure
import pytest

from src.api.json_placeholder_api_client import JSONPlaceholderClient
from src.api.models.post import Post, PostCreate, PostUpdate


@pytest.fixture(scope="module")
def api_client(config):
    """Return an instance of the JSONPlaceholder API client."""
    return JSONPlaceholderClient(config["api_base_url"])


@allure.feature("Posts API")
@pytest.mark.api
class TestGetPosts:
    """Tests for GET /posts endpoint."""

    @allure.story("GET /posts")
    @allure.title("GET /posts returns HTTP 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_posts_returns_200(self, api_client):
        """Scenario 1: GET /posts — verify response status."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass  # Client is ready via fixture

        with allure.step("When a GET request is made to /posts"):
            response = api_client.get_posts()

        with allure.step("Then the response status is 200"):
            assert response.status_code == 200

    @allure.story("GET /posts")
    @allure.title("GET /posts response body is a non-empty list")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_posts_returns_list(self, api_client):
        """Scenario 1: GET /posts — verify response structure is a list."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts"):
            response = api_client.get_posts()

        with allure.step("Then the response body is a non-empty list"):
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @allure.story("GET /posts")
    @allure.title("Every post in GET /posts response conforms to the Post schema")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_posts_item_structure(self, api_client):
        """Scenario 1: GET /posts — verify each post has required fields."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts"):
            response = api_client.get_posts()

        with allure.step("Then every item in the list is a valid Post (userId, id, title, body)"):
            posts = [Post.model_validate(p) for p in response.json()]
            assert len(posts) > 0


@allure.feature("Posts API")
@pytest.mark.api
class TestGetSinglePost:
    """Tests for GET /posts/{id} endpoint."""

    @allure.story("GET /posts/{id}")
    @allure.title("GET /posts/1 returns HTTP 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_post_returns_200(self, api_client):
        """Scenario 2: GET /posts/{id} — verify response status."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts/1"):
            response = api_client.get_post(1)

        with allure.step("Then the response status is 200"):
            assert response.status_code == 200

    @allure.story("GET /posts/{id}")
    @allure.title("GET /posts/1 returns a post with id=1")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_post_returns_correct_id(self, api_client):
        """Scenario 2: GET /posts/{id} — verify correct post is returned."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts/1"):
            response = api_client.get_post(1)

        with allure.step("Then the returned post has id=1 and matches the Post schema"):
            post = Post.model_validate(response.json())
            assert post.id == 1

    @allure.story("GET /posts/{id}")
    @allure.title("GET /posts/1 response body contains all required Post fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_post_has_required_fields(self, api_client):
        """Scenario 2: GET /posts/{id} — verify post has required fields."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts/1"):
            response = api_client.get_post(1)

        with allure.step("Then the response body conforms to the Post schema with all typed fields"):
            post = Post.model_validate(response.json())
            assert isinstance(post.userId, int)
            assert isinstance(post.id, int)
            assert isinstance(post.title, str)
            assert isinstance(post.body, str)


@allure.feature("Posts API")
@pytest.mark.api
class TestCreatePost:
    """Tests for POST /posts endpoint."""

    @allure.story("POST /posts")
    @allure.title("POST /posts returns HTTP 201 when creating a new post")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_post_returns_201(self, api_client):
        """Scenario 3: POST /posts — verify resource creation status."""
        with allure.step("Given a valid PostCreate payload"):
            payload = PostCreate(title="foo", body="bar", userId=1)

        with allure.step("When a POST request is made to /posts"):
            response = api_client.create_post(payload.model_dump())

        with allure.step("Then the response status is 201 Created"):
            assert response.status_code == 201

    @allure.story("POST /posts")
    @allure.title("POST /posts response body contains the created post with an assigned id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_post_returns_created_resource(self, api_client):
        """Scenario 3: POST /posts — verify the created resource is returned."""
        with allure.step("Given a valid PostCreate payload"):
            payload = PostCreate(title="Test Post", body="Test body content", userId=1)

        with allure.step("When a POST request is made to /posts"):
            response = api_client.create_post(payload.model_dump())

        with allure.step("Then the response body contains the created post with an assigned id"):
            created = Post.model_validate(response.json())
            assert created.title == payload.title
            assert created.body == payload.body
            assert created.userId == payload.userId
            assert isinstance(created.id, int)


@allure.feature("Posts API")
@pytest.mark.api
class TestUpdatePost:
    """Tests for PUT /posts/{id} endpoint."""

    @allure.story("PUT /posts/{id}")
    @allure.title("PUT /posts/1 returns HTTP 200 when updating an existing post")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_post_returns_200(self, api_client):
        """Scenario 4: PUT /posts/{id} — verify resource update status."""
        with allure.step("Given a valid PostUpdate payload for post id=1"):
            payload = PostUpdate(id=1, title="updated title", body="updated body", userId=1)

        with allure.step("When a PUT request is made to /posts/1"):
            response = api_client.update_post(1, payload.model_dump())

        with allure.step("Then the response status is 200"):
            assert response.status_code == 200

    @allure.story("PUT /posts/{id}")
    @allure.title("PUT /posts/1 response body reflects the updated post fields")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_post_returns_updated_resource(self, api_client):
        """Scenario 4: PUT /posts/{id} — verify updated data is returned."""
        with allure.step("Given a valid PostUpdate payload for post id=1"):
            payload = PostUpdate(id=1, title="updated title", body="updated body", userId=1)

        with allure.step("When a PUT request is made to /posts/1"):
            response = api_client.update_post(1, payload.model_dump())

        with allure.step("Then the response body reflects the updated title and body"):
            updated = Post.model_validate(response.json())
            assert updated.title == payload.title
            assert updated.body == payload.body


@allure.feature("Posts API")
@pytest.mark.api
class TestDeletePost:
    """Tests for DELETE /posts/{id} endpoint."""

    @allure.story("DELETE /posts/{id}")
    @allure.title("DELETE /posts/1 returns HTTP 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_post_returns_200(self, api_client):
        """Scenario 5: DELETE /posts/{id} — verify resource deletion."""
        with allure.step("Given post id=1 exists in the JSONPlaceholder API"):
            pass  # JSONPlaceholder always serves the resource

        with allure.step("When a DELETE request is made to /posts/1"):
            response = api_client.delete_post(1)

        with allure.step("Then the response status is 200"):
            assert response.status_code == 200

    @allure.story("DELETE /posts/{id}")
    @allure.title("DELETE /posts/1 returns an empty response body")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_post_returns_empty_body(self, api_client):
        """Scenario 5: DELETE /posts/{id} — verify response body is empty."""
        with allure.step("Given post id=1 exists in the JSONPlaceholder API"):
            pass

        with allure.step("When a DELETE request is made to /posts/1"):
            response = api_client.delete_post(1)

        with allure.step("Then the response body is an empty object"):
            assert response.json() == {}


@allure.feature("Posts API")
@pytest.mark.api
class TestFilterPosts:
    """Tests for GET /posts?userId={id} filtering endpoint."""

    @allure.story("GET /posts?userId={id}")
    @allure.title("GET /posts?userId=1 returns HTTP 200")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_posts_by_user_returns_200(self, api_client):
        """Scenario 6 (optional): GET /posts?userId={id} — verify status."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts with userId=1 query parameter"):
            response = api_client.get_posts_by_user(1)

        with allure.step("Then the response status is 200"):
            assert response.status_code == 200

    @allure.story("GET /posts?userId={id}")
    @allure.title("GET /posts?userId=1 returns only posts belonging to user 1")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_posts_by_user_returns_filtered_results(self, api_client):
        """Scenario 6 (optional): GET /posts?userId={id} — verify filtering."""
        with allure.step("Given the JSONPlaceholder API is available"):
            pass

        with allure.step("When a GET request is made to /posts with userId=1 query parameter"):
            user_id = 1
            response = api_client.get_posts_by_user(user_id)

        with allure.step("Then all returned posts belong to user 1 and conform to the Post schema"):
            posts = [Post.model_validate(p) for p in response.json()]
            assert len(posts) > 0
            for post in posts:
                assert post.userId == user_id, f"Expected userId={user_id}, got userId={post.userId}"


@allure.feature("Posts API")
@pytest.mark.api
class TestNegativeCases:
    """Negative tests for the JSONPlaceholder API."""

    @allure.story("Non-existent Resource")
    @allure.title("GET /posts/99999 returns HTTP 404 for a non-existent post")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_post_returns_404(self, api_client):
        """Scenario 7 (optional): GET non-existent resource — verify 404."""
        with allure.step("Given a post with id=99999 does not exist"):
            pass

        with allure.step("When a GET request is made to /posts/99999"):
            response = api_client.get_post(99999)

        with allure.step("Then the response status is 404 Not Found"):
            assert response.status_code == 404

    @allure.story("Non-existent Resource")
    @allure.title("GET /posts/99999 returns an empty body for a non-existent post")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_post_returns_empty_body(self, api_client):
        """Scenario 7 (optional): GET non-existent resource — verify empty body."""
        with allure.step("Given a post with id=99999 does not exist"):
            pass

        with allure.step("When a GET request is made to /posts/99999"):
            response = api_client.get_post(99999)

        with allure.step("Then the response body is an empty object"):
            assert response.json() == {}
