# Імпортуємо pytest і сам додаток Flask
import pytest
from my_flask_app import app

# Фікстура для створення тестового клієнта Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Тест для перевірки отримання наявного користувача
def test_get_existing_user(client):
    response = client.get("/api/users/user1")  # Запит до API
    assert response.status_code == 200         # Очікуємо статус 200
    data = response.get_json()                 # Отримуємо JSON з відповіді
    assert data["username"] == "user1"         # Перевіряємо, що ім’я правильне
    assert data["data"]["name"] == "Alice"     # Перевіряємо ім’я користувача
    assert data["data"]["role"] == "admin"     # Перевіряємо роль користувача

# Тест для перевірки запиту до неіснуючого користувача
def test_get_nonexistent_user(client):
    response = client.get("/api/users/user3")  # Запит до неіснуючого користувача
    assert response.status_code == 404         # Очікуємо статус 404
    data = response.get_json()
    assert "error" in data                     # Перевіряємо, що є повідомлення про помилку