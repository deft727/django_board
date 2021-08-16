from functools import partial
from logging import log
from django import urls
from django.contrib.auth import get_user_model
import pytest
from django.contrib.auth.models import User
from accounts.models import Reader,Bloger
from .conftest import create_user
from django.shortcuts import redirect
from urllib.parse import urlencode


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
def test_user_logout(client, authenticated_user):
    logout_url = urls.reverse('logout')
    resp = client.get(logout_url,follow_redirects=False)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')


@pytest.mark.django_db
def test_create_reader(client,create_reader,reader_data):
    user_model = Reader
    assert user_model.objects.count() == 1
    login_url = urls.reverse('login')
    print(login_url)
    resp = client.post(login_url,data=reader_data,follow_redirects=True)
    assert resp.status_code == 200











































































# @pytest.mark.django_db
# def test_reader_form_with_data(reader):
#     assert True is not None
#     assert True == reader.is_valid()


# @pytest.mark.django_db
# def test_bloger_form_with_data(bloger):
#     assert True is not None
#     assert True == bloger.is_valid()




# @pytest.mark.django_db
# def test_user_signup(client):
#     user_model = User
#     reader_model = Reader

#     print(user_model.objects.count(),' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#     print(reader_model.objects.count(),' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

#     assert reader_model.objects.count() == 0

#     user = create_user()
#     signupurl = client.get(urls.reverse('signup_reader'))
#     print(signupurl)
#     print(signupurl)

#     data = {'user':user,
#             'username':user.username,
#     }
#     print(data)
#     resp = client.post(signupurl,data)
#     print(resp)
#     # user = create_user()
#     # # print(reader)
#     # resp = client.post(signupurl,data = {
#     #     'password':'qwerty1234',
#     #     'confirm_password':'qwerty1234',
#     #     'user':user,
#     #     'username':user.username,
#     # })
#     # x= resp
#     # print(x)



#     # assert user_model.objects.count() == 0
#     assert resp.status_code == 302


 





# @pytest.mark.django_db
# def test_context_create_bloger(client):
#     user_model = User
#     reader_model = Bloger
#     assert user_model.objects.count() == 0
#     user = create_user()
#     assert user_model.objects.count() == 1

#     assert reader_model.objects.count() == 0
#     data = {'username':'test123','password':'djnagoresearchj929','email':'sadasdsa@mail.com','user':user}

#     url = urls.reverse("signup_bloger")
#     response = client.post(url, data)
    

#     # reader_model.objects.create(user=user,username=response.context['form'].cleaned_data['username'])
#     # assert reader_model.objects.count() == 1
#     assert response.status_code == 302




    # user = create_user()
    # resp = Reader(username=user.username,user=user)
    # resp.set_password='qwerty1234'
    # resp.save()
    # print(resp)




