import pytest 
from .models import Country, Mountain

@pytest.mark.django_db
def test_guest(api_client, country):
    response = api_client.get("/api/v1/countries")
    assert response.status_code == 200 
    assert {"id": country.id, "name": country.name, "description": country.description} in response.data

@pytest.mark.django_db
def test_cannot_create(api_client):
    response = api_client.post("/api/v1/countries", {"name": "Ukraine", "description": "test"}, format="json")
    assert response.status_code == 401
    assert not Country.objects.filter(name="Ukraine").exists()

@pytest.mark.django_db
def test_regular_user_cannot_create(api_client, regular_usr):
    response = api_client.post("/api/v1/token/", {"username": regular_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.post("/api/v1/countries", {"name": "Ukraine", "description": "test"}, format="json")
    assert response.status_code == 403
    assert not Country.objects.filter(name="Ukraine").exists()

@pytest.mark.django_db
def test_guest_detail(api_client, country):
    response = api_client.get(f"/api/v1/countries/{country.id}")
    assert response.status_code == 200
    assert response.data == {"id": country.id, "name": country.name, "description": country.description}

@pytest.mark.django_db
def test_admin_create(api_client, admin_usr):
    response = api_client.post("/api/v1/token/", {"username": admin_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.post("/api/v1/countries", {"name": "Poland", "description": "test"}, format="json")
    assert response.status_code == 201
    assert Country.objects.filter(id=response.data["id"], name="Poland").exists()

@pytest.mark.django_db
def test_admin_patch(api_client, admin_usr, country):
    response = api_client.post("/api/v1/token/", {"username": admin_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.patch(f"/api/v1/countries/{country.id}", {"description": "Новий опис"}, format="json")
    assert response.status_code == 200
    assert Country.objects.filter(id=country.id, name=country.name, description="Новий опис").exists()

@pytest.mark.django_db
def test_admin_delete(api_client, admin_usr, country):
    response = api_client.post("/api/v1/token/", {"username": admin_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.delete(f"/api/v1/countries/{country.id}")
    assert response.status_code == 204
    assert not Country.objects.filter(id=country.id).exists()

@pytest.mark.django_db
def test_duplicate_name(api_client, admin_usr, country):
    response = api_client.post("/api/v1/token/", {"username": admin_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.post("/api/v1/countries", {"name": country.name, "description": "test"}, format="json")
    assert response.status_code == 400
    assert "name" in response.data["errors"]
    assert Country.objects.filter(name=country.name).count() == 1

@pytest.mark.django_db
def test_delete_missing_country(api_client, admin_usr, country):
    country_id = country.id
    country.delete()
    response = api_client.post("/api/v1/token/", {"username": admin_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.delete(f"/api/v1/countries/{country_id}")
    assert response.status_code == 404
    assert "errors" in response.data

@pytest.mark.django_db
def test_delete_country_with_mountain(api_client, admin_usr, country):
    mountain = Mountain.objects.create(country=country, name="Говерла", height=2061, description="test")
    response = api_client.post("/api/v1/token/", {"username": admin_usr.username, "password": "TestPassword123!"}, format="json")
    assert response.status_code == 200
    tokens = response.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.delete(f"/api/v1/countries/{country.id}")
    assert response.status_code == 409
    assert Country.objects.filter(id=country.id).exists()
    assert Mountain.objects.filter(id=mountain.id, country_id=country.id).exists()