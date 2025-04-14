import unittest

# Функція додавання
def add(x, y):
    return x + y

# Тести для функції add
class TestAddition(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(3, 5), 8)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -2), -3)

    def test_add_zero(self):
        self.assertEqual(add(0, 0), 0)

    def test_add_mixed(self):
        self.assertEqual(add(-1, 1), 0)

# Клас Калькулятора з методами додавання та віднімання
class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, x):
        self.value += x
        return self.value

    def subtract(self, x):
        self.value -= x
        return self.value

# Тести для класу Calculator
class TestCalculator(unittest.TestCase):
    def setUp(self):
        # Ініціалізація перед кожним тестом
        self.calc = Calculator()

    def tearDown(self):
        # Видалення екземпляра після тесту
        del self.calc

    def test_add(self):
        self.assertEqual(self.calc.add(5), 5)
        self.assertEqual(self.calc.add(3), 8)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5), -5)

# Клас для сервісу аутентифікації
class AuthenticationService:
    """
    Сервіс аутентифікації, який перевіряє введені дані за даними з бази.
    """
    def __init__(self, user_db):
        self.user_db = user_db

    def _get_user(self, username):
        """
        Симулює отримання даних користувача із бази даних.
        """
        return self.user_db.get(username)

    def authenticate(self, username, password):
        """
        Якщо користувач існує та пароль вірний, повертає True, інакше False.
        """
        user = self._get_user(username)
        if user and user.get("password") == password:
            return True
        return False

# Тести для AuthenticationService
from unittest.mock import patch

class TestAuthenticationService(unittest.TestCase):
    def setUp(self):
        # Створюємо фіктивну "базу даних"
        self.fake_db = {
            "user1": {"password": "pass123"},
            "user2": {"password": "secret"},
        }
        self.auth_service = AuthenticationService(self.fake_db)

    def test_authenticate_success(self):
        # Успішна аутентифікація
        self.assertTrue(self.auth_service.authenticate("user1", "pass123"))

    def test_authenticate_failure_wrong_password(self):
        # Невірний пароль
        self.assertFalse(self.auth_service.authenticate("user1", "wrong"))

    def test_authenticate_failure_no_user(self):
        # Користувача немає
        self.assertFalse(self.auth_service.authenticate("nonexistent", "any_password"))

    @patch.object(AuthenticationService, "_get_user")
    def test_authenticate_with_mock(self, mock_get_user):
        # Мокаємо метод _get_user
        mock_get_user.return_value = {"password": "dynamic"}
        self.assertTrue(self.auth_service.authenticate("dummy", "dynamic"))
        mock_get_user.assert_called_once_with("dummy")

if __name__ == '__main__':
    unittest.main()
