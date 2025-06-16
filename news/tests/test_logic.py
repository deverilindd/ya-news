# test_logic.py
import pytest

from pytest_django.asserts import assertRedirects
from http import HTTPStatus

from django.urls import reverse

# Дополнительно импортируем функцию slugify.
from pytils.translit import slugify

# Импортируем функции для проверки редиректа и ошибки формы:
from pytest_django.asserts import assertRedirects, assertFormError

# Импортируем из модуля forms сообщение об ошибке:
from news.forms import WARNING

from news.models import News


# Анонимный пользователь не может отправить комментарий.

# Авторизованный пользователь может отправить комментарий.
def test_user_can_create_note(author_client, author, form_data):
    url = reverse('news:detail')
    response = author_client.post(url, data=form_data)
# Если комментарий содержит запрещённые слова, он не будет опубликован, а форма вернёт ошибку.

# Авторизованный пользователь может редактировать или удалять свои комментарии.

# Авторизованный пользователь не может редактировать или удалять чужие комментарии.