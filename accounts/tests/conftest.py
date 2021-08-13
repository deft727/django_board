import pytest
from django.contrib.auth.models import User
from accounts.forms import ReaderForm, SignUpFormReader,SignUpFormBloger
from accounts.models import Reader,Bloger
# @pytest.mark.django_db



@pytest.fixture
def reader_data():
    return {'username':'test123','password':'djnagoresearchj929','email':'sadasdsa@mail.com'}

    
@pytest.mark.django_db
def create_user():
    user = User.objects.create(username='teslogin',password='qwerty1234',email='sadasd@gmail.com')
    return user



@pytest.fixture
def reader():

    user = User.objects.create(username="james", password="password")

    obj = Reader.objects.create(user=user,username=user.username)
    
    data = {
        'user':user,
        'username':obj.username,
    }
    form = SignUpFormReader(data=data)
    yield form



@pytest.fixture
def bloger():

    user = User.objects.create(username="james", password="password")

    obj = Bloger.objects.create(user=user,username=user.username)
    
    data = {
        'user':user,
        'username':obj.username,
    }
    form =SignUpFormBloger(data=data)
    yield form
