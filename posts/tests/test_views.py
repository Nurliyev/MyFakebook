import os
import shutil
from django.test import Client, TestCase, override_settings
from MyFakebook.settings import BASE_DIR
from django.urls import reverse

from posts.models import Post
from posts.views import PostList, LikeView
from profiles.models import User

TEST_MEDIA_ROOT = os.path.join(BASE_DIR, "articles/tests/media/")


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="username", password="password", email="example@email.com", is_active=True,
        )

        self.article_create_path = reverse("post-create")
        self.article_list_path = reverse("post-list")
        self.article_like_path = reverse("like-button")

        self.client.force_login(self.user)

        return super().setUp()

    def tearDown(self):
        # Deletes created media files after each test
        shutil.rmtree(f"{TEST_MEDIA_ROOT}/images/", ignore_errors=True)

        return super().tearDown()


class TestArticleListView(BaseTestCase):
    def setUp(self):
        self.author = User.objects.create(
            email="user@email.com",
            username="user",
            password="password",
            is_active=True,
        )

        for title_num in range(1, 15):
            Post.objects.create(
                content="This is a article content",
                avatar="banner.png",
                author=self.author,
            )

        return super(TestArticleListView, self).setUp()

    def test_url_exists(self):
        response = self.client.get(self.article_list_path)

        self.assertEqual(response.resolver_match.func.__name__, PostList.as_view().__name__)
        self.assertEqual(response.status_code, 200)

    def test_url_exists_without_auth(self):
        self.client.logout()
        response = self.client.get(self.article_list_path)
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.article_list_path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post-list.html")

    def test_view_object_list_is_correct(self):
        response = self.client.get(self.article_list_path)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("posts" in response.context)
        self.assertTrue(len(response.context["posts"]) == 3)

    def test_correct_page_with_pagination_query_params(self):
        # Get second page and confirm it has (exactly) remaining 4 items
        response = self.client.get(self.article_list_path, {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["posts"]) == 3)


class TestArticleLikeView(BaseTestCase):
    def setUp(self):
        self.author = User.objects.create(
            email="author@email.com",
            username="author",
            password="password",
            is_active=True,
        )
        self.post = Post.objects.create(
            content="This is a article content",
            avatar="banner.png",
            author=self.author,
        )

        return super().setUp()

    def post_like(self):
        response = self.client.post(
            self.article_like_path,
            {"id": self.post.id},
            content_type="application/json",
        )

        return response

    def test_users_can_like_articles(self):
        response = self.post_like()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, LikeView.as_view().__name__)
        self.assertEqual(response.json(), {"total_likes": 1, "is_liked": True})

    def test_users_can_remove_like_from_articles(self):
        for _ in range(2):
            response = self.post_like()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"total_likes": 0, "is_liked": False})

    def test_anonymous_users_cannot_like_articles(self):
        self.client.logout()

        response = self.post_like()

        self.assertEqual(response.status_code, 403)

    def test_with_invalid_article_id(self):
        response = self.client.post(
            self.article_like_path, {"id": 999}, content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)

    def test_get_request(self):
        response = self.client.get(self.article_like_path)

        self.assertEqual(response.status_code, 405)
