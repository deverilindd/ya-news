import pytest
from http import HTTPStatus
from pytest_lazy_fixtures import lf
from django.urls import reverse
from django.conf import settings


from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(news_base, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert  news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(news_base, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates==sorted_dates


@pytest.mark.django_db
def test_comments_order(news, comment_base, author_client):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps==sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(news, client):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(news, author_client):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
