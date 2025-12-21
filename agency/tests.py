from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic, Newspaper


class PublicViewTests(TestCase):
    def test_login_required(self):
        """Перевірка, що неавторизований користувач перенаправляється на сторінку логіну"""
        res = self.client.get(reverse("agency:index"))
        self.assertNotEqual(res.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        # Створюємо тестового користувача
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            years_of_experience=5
        )
        self.client.login(username="test_user", password="test_password")

    def test_retrieve_index_page(self):
        """Перевірка доступності головної сторінки після авторизації"""
        res = self.client.get(reverse("agency:index"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "agency/index.html")

    def test_topic_list_view(self):
        """Перевірка відображення списку тем"""
        Topic.objects.create(name="Politics")
        res = self.client.get(reverse("agency:topic-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Politics")


class ModelTests(TestCase):
    def test_redactor_str(self):
        """Перевірка рядкового представлення моделі Redactor"""
        redactor = get_user_model().objects.create_user(
            username="editor1",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(str(redactor), "editor1 (John Doe)")

    def test_topic_str(self):
        """Перевірка рядкового представлення моделі Topic"""
        topic = Topic.objects.create(name="Science")
        self.assertEqual(str(topic), "Science")


class NewspaperFormTests(TestCase):
    def setUp(self):
        # 1. Створюємо тему та користувача
        self.topic = Topic.objects.create(name="Culture")
        self.user = get_user_model().objects.create_user(
            username="test_editor",
            password="password123"
        )
        # 2. Обов'язково логінимо користувача, щоб уникнути Redirect 302
        self.client.login(username="test_editor", password="password123")

    def test_newspaper_search_form(self):
        """Перевірка пошуку в списку газет"""
        Newspaper.objects.create(
            title="Morning News",
            content="Text",
            topic=self.topic
        )
        Newspaper.objects.create(
            title="Evening Post",
            content="Text",
            topic=self.topic
        )

        res = self.client.get(reverse("agency:newspaper-list"), {"title": "Morning"})

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Morning News")
        self.assertNotContains(res, "Evening Post")