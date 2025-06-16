# test_routes.py
import pytest

from http import HTTPStatus
from pytest_lazy_fixtures import lf
from pytest_django.asserts import assertRedirects

from django.urls import reverse


# Главная страница доступна анонимному пользователю.
# Страница отдельной новости доступна анонимному пользователю.
# Страницы регистрации пользователей, входа в учётную запись и
# выхода из неё доступны анонимным пользователям.
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'news:home',
        'news:detail',
        'users:login',
        'users:logout',
        'users:signup',
    )
)
def test_pages_availability_for_anonymous_user(client, news, name):
    url = reverse(name, args=(news.id,) if name == 'news:detail' else None)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# Страницы удаления и редактирования комментария доступны автору комментария.
# Авторизованный пользователь не может зайти на страницы редактирования или
# удаления чужих комментариев (возвращается ошибка 404).
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    (
        'news:delete',
        'news:edit',
    )
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, expected_status, id_for_comment, name
):
    url = reverse(name, args=id_for_comment)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


# При попытке перейти на страницу редактирования или удаления комментария
# анонимный пользователь перенаправляется на страницу авторизации.
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        'news:delete',
        'news:edit',
    )
)
def test_redirects(client, name, id_for_comment):
    login_url = reverse('users:login')
    url = reverse(name, args=id_for_comment)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
