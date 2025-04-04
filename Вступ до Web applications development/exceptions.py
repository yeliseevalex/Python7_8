"""
Цей файл демонструє приклади роботи з обробкою виключень, перевіркою даних,
розгалуженням логіки в try/except/else/finally, використанням assert,
наслідуванням виключень та роботою з кастомним логуванням та базою даних.
"""

#############################################
# 1. Функція ділення без обробки виключень
#############################################
def divide_without_exception(a, b):
    # Повертає результат ділення a на b.
    # Якщо b = 0, виключення не обробляється і програма зупиниться.
    return a / b

#############################################
# 2. Функція ділення з обробкою виключення ZeroDivisionError
#############################################
def divide_with_exception(a, b):
    try:
        # Намагання виконати ділення
        return a / b
    except ZeroDivisionError:
        # Якщо сталася помилка ділення на нуль, виводимо повідомлення та повертаємо None.
        print("Помилка: ділення на нуль!")
        return None

#############################################
# 3. Функція ділення з блоками try/except/else/finally
#############################################
def divide(a, b):
    try:
        # Спроба виконати ділення a на b
        result = a / b
    except ZeroDivisionError:
        # Якщо b = 0, виводимо повідомлення про помилку і повертаємо None.
        print("Помилка: ділення на нуль!")
        return None
    else:
        # Якщо виключення не виникло, виводимо повідомлення про успішне виконання.
        print("Ділення виконано успішно!")
        return result
    finally:
        # Блок finally виконується завжди, незалежно від того, чи було виключення.
        print("Операція ділення завершена")

#############################################
# 4. Функції перевірки позитивного числа
#############################################
def check_positive_without_raise(number):
    # Повертає число без перевірки.
    return number

def check_positive_with_raise(number):
    # Якщо число менше 0, викликаємо помилку ValueError.
    if number < 0:
        raise ValueError("Число має бути додатнім!")
    # Якщо число додатнє, повертаємо його.
    return number

#############################################
# 5. Функції обчислення середнього значення списку чисел
#############################################
def calculate_avg_without_assert(numbers):
    # Обчислює середнє значення чисел у списку.
    # Якщо список порожній, виникне ZeroDivisionError.
    return sum(numbers) / len(numbers)

def calculate_avg_with_assert(numbers):
    # Перевіряємо, що список не порожній, інакше викликаємо AssertionError.
    assert len(numbers) > 0, "Список чисел не може бути порожнім"
    return sum(numbers) / len(numbers)

#############################################
# 6. Функція обробки введених даних
#############################################
def process_input(value):
    # Перевіряємо, що значення є числом (int або float).
    # Якщо ні, викликаємо AssertionError з відповідним повідомленням.
    assert isinstance(value, (int, float)), "67. Очікується число"
    # Повертаємо подвоєне значення.
    return value * 2

#############################################
# 7. Функції для демонстрації наслідування виключень (ланцюжок помилок)
#############################################
def function_c():
    # Викликає виключення KeyError з повідомленням.
    raise KeyError("Missing key in the JSON")

def function_b():
    try:
        # Викликаємо функцію function_c, яка викликає KeyError.
        function_c()
    except KeyError as e:
        # Перехоплюємо KeyError і викликаємо ValueError, наслідуючи помилку.
        raise ValueError("Invalid value") from e

def function_a():
    try:
        # Викликаємо function_b, яка може викликати ValueError.
        function_b()
    except ValueError as e:
        # Перехоплюємо ValueError і викликаємо RuntimeError, наслідуючи помилку.
        raise RuntimeError("Error while processing request") from e

#############################################
# 8. Функція перевірки введених даних користувача
#############################################
def validate_user_input(user_input):
    # Перевіряємо, що введене значення є числом і більше 0.
    if not isinstance(user_input, int) or user_input <= 0:
        raise ValueError("Невірний формат вхідних даних")
    return user_input

#############################################
# 9. Функція для обробки платежу
#############################################
def process_payment(amount, balance):
    try:
        # Якщо сума платежу перевищує баланс, викликаємо ValueError.
        if amount > balance:
            raise ValueError("Недостатньо коштів для оплати")
        # Обчислюємо новий баланс.
        new_balance = balance - amount
    except ValueError as e:
        # Якщо сталася помилка, виводимо повідомлення про помилку і повертаємо None.
        print(f"Помилка платежу {e}")
        return None
    else:
        # Якщо помилки не виникло, повертаємо новий баланс.
        return new_balance

#############################################
# 10. Функція для отримання даних користувача з бази даних SQLite
#############################################
import sqlite3
def fetch_user_data(user_id):
    connection = None  # Ініціалізуємо змінну для з'єднання з базою даних.
    try:
        # Підключаємось до бази даних "example.db".
        connection = sqlite3.connect("example.db")
        cursor = connection.cursor()  # Отримуємо об'єкт курсора для виконання запитів.
        # Виконуємо SQL-запит для отримання даних користувача за заданим user_id.
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        data = cursor.fetchone()  # Отримуємо перший рядок результату.
        # Якщо дані не знайдено, викликаємо LookupError.
        if data is None:
            raise LookupError("Користувача не знайдено")
    except sqlite3.DatabaseError as e:
        # Перехоплюємо помилки бази даних та виводимо повідомлення.
        print(f"Помилка бази даних {e}")
        return None
    else:
        # Якщо запит успішний, повертаємо дані користувача.
        return data
    finally:
        # Закриваємо з'єднання з базою даних, якщо воно було встановлено.
        if connection:
            connection.close()
            print("З'єднання з базою даних закрито")

#############################################
# 11. Кастомізоване виключення для аутентифікації
#############################################
class AuthenticationError(Exception):
    def __init__(self, message="Аутентифікація не пройдена"):
        # Ініціалізуємо батьківський клас Exception з повідомленням.
        super().__init__(message)

def authentication_user(username, password):
    # Перевіряємо, чи співпадають логін і пароль із очікуваними значеннями.
    if username != 'admin' or password != '12345':
        raise AuthenticationError("Невірні дані!")
    return True

#############################################
# 12. Функція для обробки API-запиту з кастомним логуванням
#############################################
import logging
from http import HTTPStatus

# Налаштовуємо базовий рівень логування.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Кастомізоване виключення для API.
class APIError(Exception):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        # Ініціалізуємо Exception та додаємо статус код.
        super().__init__(message)
        self.status_code = status_code

def process_api_request(data):
    try:
        # Перевіряємо, чи присутній параметр "user_id" у вхідних даних.
        if "user_id" not in data:
            raise APIError("Відсутній параметр 'user_id'", HTTPStatus.UNPROCESSABLE_ENTITY)
        # Перевіряємо, чи є 'amount' числом і більше 0.
        if not isinstance(data.get('amount'), (int, float)) or data.get("amount") <= 0:
            raise APIError("Некоректне значення 'amount'", HTTPStatus.BAD_REQUEST)
        # Формуємо результат обчислення нового балансу (це лише приклад).
        result = {"user_id": data["user_id"], "new_balance": 100 - data["amount"]}
    except APIError as e:
        # Якщо виникла помилка API, логікуємо помилку та повертаємо словник з інформацією.
        logger.error(f"APIError: {e} (HTTP {e.status_code})")
        return {"error": str(e), "status": e.status_code}
    else:
        # Якщо запит оброблено успішно, логікуємо інформаційне повідомлення та повертаємо результат.
        logger.info(f"Запит оброблено успішно (HTTP {HTTPStatus.OK})")
        return {"data": result, "status": HTTPStatus.OK}

#############################################
# Основний блок виконання (if __name__ == '__main__')
#############################################
if __name__ == '__main__':
    print("=== Демонстрація роботи виключень та обробки даних ===\n")

    # 1. Ділення без обробки виключень.
    # (Цей виклик може зупинити програму, якщо ділення на нуль)
    print("1. Ділення без обробки виключень:")
    print(divide_without_exception(10, 5))   # Очікується: 2.0
    print(divide_without_exception(0, 5))    # Очікується: 0.0
    # Наступний виклик викличе ZeroDivisionError, тому коментуємо його для подальшого виконання.
    # print(divide_without_exception(10, 0))
    print()

    # 2. Ділення з обробкою виключення.
    print("2. Ділення з обробкою виключення:")
    print(divide_with_exception(10, 0))      # Очікується: Помилка: ділення на нуль! та None
    print(divide_with_exception(10, 5))      # Очікується: 2.0
    print()

    # 3. Ділення з блоками try/except/else/finally.
    print("3. Ділення з try/except/else/finally:")
    print(divide(10, 5))     # Очікується: Вивід повідомлень та результат 2.0
    print('-' * 20)
    print(divide(10, 0))     # Очікується: Повідомлення про помилку та None
    print()

    # 4. Перевірка позитивного числа.
    print("4. Перевірка позитивного числа:")
    print(check_positive_without_raise(10))   # Повертає 10
    try:
        print(check_positive_with_raise(-5))    # Викличе ValueError
    except ValueError as e:
        print(e)
    print()

    # 5. Обчислення середнього значення списку чисел.
    print("5. Обчислення середнього значення:")
    print(calculate_avg_without_assert([1, 2, 3]))  # 2.0
    try:
        print(calculate_avg_with_assert([]))        # Викличе AssertionError
    except AssertionError as e:
        print(e)
    print()

    # 6. Обробка введених даних.
    print("6. Обробка введених даних:")
    print(process_input(5))       # Повертає 10
    try:
        print(process_input("text"))  # Викличе AssertionError
    except AssertionError as e:
        print(e)
    print()

    # 7. Демонстрація наслідування виключень.
    print("7. Демонстрація ланцюжка виключень:")
    try:
        function_a()
    except RuntimeError as e:
        print(f"Main error: {e}")
        # Виводимо ланцюжок причин помилки.
        cause = e.__cause__
        while cause:
            print(cause)
            cause = cause.__cause__
    print()

    # 8. Перевірка вхідних даних користувача.
    print("8. Перевірка введених даних користувача:")
    try:
        print(validate_user_input("abc"))  # Викличе ValueError
    except ValueError as e:
        print(e)
    print(validate_user_input(10))           # Повертає 10
    print()

    # 9. Обробка платежу.
    print("9. Обробка платежу:")
    print(process_payment(100, 100))         # Очікується: 0
    print(process_payment(150, 100))         # Очікується: повідомлення про помилку та None
    print()

    # 10. Отримання даних користувача з бази даних.
    print("10. Отримання даних користувача з бази даних:")
    user = fetch_user_data(1)  # Передбачається, що база даних "example.db" існує
    if user:
        print(f"Дані користувача: {user}")
    else:
        print("Помилка при отриманні даних користувача")
    print()

    # 11. Аутентифікація користувача.
    print("11. Аутентифікація користувача:")
    try:
        authentication_user("admin", "12345")  # Повинно пройти аутентифікацію
        print("Аутентифікація пройшла успішно!")
    except AuthenticationError as e:
        print(e)
    print()

    # 12. Обробка API-запиту з кастомним логуванням.
    print("12. Обробка API-запиту:")
    print(process_api_request({"amount": 50}))  # Відсутній user_id, очікується помилка
    print(process_api_request({"user_id": "123", "amount": -50}))  # Некоректне значення amount
    print(process_api_request({"user_id": "123", "amount": 50}))   # Успішний запит
    print()
