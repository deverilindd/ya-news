# conftest.py
from datetime import datetime, timedelta
import pytest

from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.test.client import Client

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=datetime.today(),
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст новости',
        created=datetime.today(),
    )
    return comment


@pytest.fixture
def id_for_comment(comment):
    return (comment.id,)


@pytest.fixture
def news_base():
    today = timezone.now()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return News.objects.all()


@pytest.fixture
def comment_base(news, author):
    now = timezone.now()
    all_comments = [
        Comment(
            news=news,
            author=author,
            text=f'Текст {i}',
            created=now + timedelta(days=i)
        )
        for i in range(10)
    ]
    Comment.objects.bulk_create(all_comments)
    return Comment.objects.all()


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
        'created': datetime.today()
    }
