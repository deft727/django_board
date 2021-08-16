import pytest
from django.contrib.auth.models import User
from accounts.forms import ReaderForm, SignUpFormReader,SignUpFormBloger
from accounts.models import Reader,Bloger
# @pytest.mark.django_db
from django.contrib.auth import get_user_model



@pytest.fixture
def reader_data():
    return {'username':'test123','password':'djnagoresearchj929',}

    
@pytest.mark.django_db
def create_user():
    user = User.objects.create(username='teslogin',password='qwerty1234',email='sadasd@gmail.com')
    return user



@pytest.fixture
def reader():

    user = User.objects.create(username='teslogiqn',password='qwerty1234',email='sadasdq@gmail.com')

    # obj = Reader.objects.create(user=user,username=user.username)
    
    data = {
        'username':'testuser',
        'email':'asdasdasc@gmail.com'
    }
    form = SignUpFormReader(data=data)
    form.user= user
    yield form




@pytest.fixture
def create_reader(reader_data):
    user_model = get_user_model()
    user = user_model.objects.create(**reader_data)
    test_user = Reader(user=user,username=user.username)
    test_user.user.set_password(reader_data.get('password'))
    test_user.save()
    return test_user



@pytest.fixture
def authenticated_user(reader_data):
    user_model = get_user_model()
    user = user_model.objects.create(**reader_data)
    test_user = Reader(user=user,username=user.username)
    test_user.user.set_password(reader_data.get('password'))
    test_user.save()
    return test_user

# @pytest.fixture
# def bloger():

#     user = User.objects.create(username="james", password="password",email='testbloge@gmail.com')

#     obj = Bloger.objects.create(user=user,username=user.username)
    
#     data = {
#         'user':user,
#         'username':obj.username,
#     }
#     form =SignUpFormBloger(data=data)
#     yield form
