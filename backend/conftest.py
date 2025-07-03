import pytest
from users.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='thiago',
        email='thiago@example.com',
        password='fire123'
    )
