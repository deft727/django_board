from django import urls
from django.contrib.auth import get_user_model
import pytest
from django.contrib.auth.models import User
from accounts.models import Reader,Bloger
from conftest import create_user


@pytest.mark.django_db
@pytest.mark.parametrize("param",[
    ('home'),
    ('signup'),
    ('signup_reader'),
    ('signup_bloger'),
    ('login'),
    ('password_reset'),
])


def test_render_views(client,param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(client):
    resp = client.get(urls.reverse('logout'))
    assert resp.status_code == 302


@pytest.mark.django_db
def test_reader_form_with_data(reader):
    assert True is not None
    assert True == reader.is_valid()



@pytest.mark.django_db
def test_bloger_form_with_data(bloger):
    assert True is not None
    assert True == bloger.is_valid()









# @pytest.mark.django_db
# def test_user_signup(client,reader_data):
#     user_model = User
#     reader_model = Reader

#     print(user_model.objects.count(),' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#     print(reader_model.objects.count(),' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

#     assert user_model.objects.count() == 0
    
#     signupurl = client.get(urls.reverse('signup_reader'))

#     # user = create_user()
#     print(reader_data)
#     resp = client.post(signupurl,reader_data)
#     x= resp
#     print(x)



#     assert user_model.objects.count() == 0
#     assert resp.status_code == 404









    # user = create_user()
    # resp = Reader(username=user.username,user=user)
    # resp.set_password='qwerty1234'
    # resp.save()
    # print(resp)

