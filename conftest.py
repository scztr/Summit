import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from catalog.models import Country

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def regular_usr(db):
    return User.objects.create_user(username="climber", password="TestPassword123!")

@pytest.fixture
def admin_usr(db):
    return User.objects.create_user(username="admin", password="TestPassword123!", is_staff=True)

@pytest.fixture
def country(db):
    return Country.objects.create(name="Ukraine", description="test")