import pytest
from django.contrib.auth.models import User

# @pytest.mark.django_db



@pytest.fixture
def reader_data():
    return {'username':'username123','password':'userpass543'}





    
@pytest.mark.django_db
def create_user():
    user = User.objects.create(username='teslogin',password='qwerty1234',email='sadasd@gmail.com')
    return user