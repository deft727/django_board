import django
from .utils import division
import pytest
from django.contrib.auth.models import User



@pytest.mark.parametrize("a,b,expected_result",[(10,2,5),
                                                (20,10,2),
                                                (30,-3,-10),
                                                (5,2,2.5)])
def test_division_good(a,b,expected_result):
    assert division(a,b) == expected_result


@pytest.mark.django_db
def test_user_count():
    assert User.objects.count() == 0



# class UserTest():
#     def setUp(self):
#         self.username = "testuser"
#         self.email = "testuser@testbase.com"
#         self.first_name = "Test"
#         self.last_name = "User"
#         self.password = "z"

#         self.test_user = User.objects.create_user(
#             username=self.username,
#             email=self.email,
#             first_name=self.first_name,
#             last_name=self.last_name
#         )

#     def test_create_user(self):
#         assert isinstance(self.test_user, User)

#     def test_default_user_is_active(self):
#         assert self.test_user.is_active

#     def test_default_user_is_staff(self):
#         assert not self.test_user.is_staff

#     def test_default_user_is_superuser(self):
#         assert not self.test_user.is_superuser

#     def test_get_full_name(self):
#         assert self.test_user.get_full_name() == 'Test User'

#     def test_get_short_name(self):
#         assert self.test_user.get_short_name() == self.email

#     def test_unicode(self):
#         assert self.test_user.__unicode__() == self.username