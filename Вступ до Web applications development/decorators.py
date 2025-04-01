"""
У цьому файлі наведено приклади функцій, обробки запитів, кешування, декораторів
"""

#############################################
# 1. Функція додавання чисел
#############################################
def add(a, b):
    # Функція, що повертає суму двох чисел a та b.
    return a + b

#############################################
# 2. Обробка HTTP-запитів: GET та POST
#############################################
def handle_get(request):
    # Функція для обробки GET-запиту.
    return "GET Response"

def handle_post(request):
    # Функція для обробки POST-запиту.
    return "POST Response"

# Словник, який зіставляє HTTP-методи з відповідними обробниками.
routers = {
    'GET': handle_get,
    'POST': handle_post
}

def process_request(method, request):
    # Функція, що обробляє запит відповідно до HTTP-методу.
    # Отримуємо обробник з словника routers за методом.
    handler = routers.get(method)
    if handler:
        # Якщо обробник знайдено, викликаємо його з запитом.
        return handler(request)
    # Якщо метод не підтримується, повертаємо повідомлення про помилку.
    return "405 Method Not Allowed"

#############################################
# 3. Функція для обробки списку даних
#############################################
def process_list(data):
    # Внутрішня функція, що перевіряє, чи є число додатнім.
    def is_positive(x):
        return x > 0
    # Повертаємо список, що містить лише додатні числа.
    return [x for x in data if is_positive(x)]

#############################################
# 4. Функція для обробки введених даних користувача
#############################################
def process_user_input(input_data):
    # Внутрішня функція для валідації кожного поля.
    def validate(field, value):
        # Якщо значення порожнє, викликаємо помилку.
        if not value:
            raise ValueError(f"Поле {field} не може бути порожнім")
        # Повертаємо значення без зайвих пробілів.
        return value.strip()

    process_data = {}  # Створюємо словник для оброблених даних.
    # Проходимо по кожному полю у вхідних даних.
    for field, value in input_data.items():
        process_data[field] = validate(field, value)
    # Повертаємо оброблений словник.
    return process_data

#############################################
# 5. Функція застосування операції до двох чисел
#############################################
def apply_operation(a, b, operation):
    # Викликаємо передану функцію операції з аргументами a та b.
    return operation(a, b)

def subtract(a, b):
    # Функція для віднімання: повертає результат a - b.
    return a - b

#############################################
# 6. Фільтрація записів згідно певного критерію
#############################################
def filter_records(records, criteria_func):
    # Повертаємо список записів, для яких функція criteria_func повертає True.
    return [record for record in records if criteria_func(record)]

def is_active_user(user):
    # Перевіряємо, чи користувач активний (ключ "active" має значення True).
    return user.get("active", False)

#############################################
# 7. Фабрика функцій привітання
#############################################
def greeting_factory(greeting):
    # Функція-фабрика, що повертає функцію привітання із заданим текстом.
    def greet(name):
        # Функція, що повертає рядок привітання для заданого імені.
        return f"{greeting}, {name}"
    return greet

#############################################
# 8. Декоратори для логування помилок (Logger 1)
#############################################
def error(message):
    # Функція для виведення повідомлення про помилку з префіксом [ERROR].
    print(f'[ERROR] {message}')

def error_handler_factory(func_error):
    # Фабрика декораторів, що приймає функцію логування помилок.
    def error_handler(func):
        # Декоратор, що обгортає функцію для обробки виключень.
        def wrapper(order):
            try:
                # Викликаємо основну функцію.
                return func(order)
            except Exception as e:
                # Логування помилки.
                func_error(f"Error in {func.__name__}: {e}")
        return wrapper
    return error_handler

# Створюємо декоратор для обробки помилок.
handle_error = error_handler_factory(error)

@handle_error
def process_order(order):
    # Функція для обробки замовлення.
    # Якщо значення "amount" менше або дорівнює 0, викликаємо помилку.
    if order.get("amount", 0) <= 0:
        raise ValueError("Amount <= 0")
    return "Order processed"

#############################################
# 9. Декоратори для логування помилок (Logger 2)
#############################################
def error_handler_factory_logger(logger):
    # Фабрика декораторів з кастомним логуванням.
    def error_handler(func):
        def wrapper(*args, **kwargs):
            try:
                # Виконуємо основну функцію.
                return func(*args, **kwargs)
            except Exception as e:
                # Логування помилки через метод error об'єкта logger.
                logger.error(f"Error in {func.__name__}: {e}")
                return None
        return wrapper
    return error_handler

# Простий логер для демонстрації.
class SimpleLogger:
    def error(self, message):
        # Метод для виведення повідомлення про помилку.
        print(f"[ERROR] {message}")

# Створюємо об'єкт логера.
logger = SimpleLogger()
# Створюємо декоратор для обробки помилок із логером.
handle_error_logger = error_handler_factory_logger(logger)

@handle_error_logger
def process_order_logger(order):
    # Функція для обробки замовлення із можливими виключеннями.
    if order.get("amount", 0) <= 0:
        raise ValueError("Неприпустиме значення amount")
    return "Order processed"

#############################################
# 10. Обробка замовлень з використанням try/except
#############################################
def process_order1(order):
    # Функція для обробки замовлення; викликає помилку, якщо amount <= 0.
    if order.get("amount", 0) <= 0:
        raise ValueError("Amount <= 0")
    return "Order processed"

#############################################
# 11. Декоратор для обмеження кількості викликів (Rate Limit)
#############################################
def rate_limited(limit):
    # Фабрика декораторів, що обмежує кількість викликів функції.
    calls = 0  # Лічильник викликів.
    def decorator(func):
        nonlocal calls  # Дозволяємо змінювати змінну calls.
        def wrapper(*args, **kwargs):
            nonlocal calls
            if calls >= limit:
                # Якщо викликів більше або дорівнює ліміту, викликаємо виключення.
                raise Exception("Rate limit exceeded")
            calls += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limited(limit=3)
def api_request(endpoint):
    # Функція для симуляції API-запиту до заданого endpoint.
    return f"Response from {endpoint}"

#############################################
# 12. Декоратор для простого кешування результатів функції
#############################################
from time import sleep

def simple_cache(func):
    # Декоратор для кешування результатів функції.
    cache = {}  # Словник для збереження кешованих результатів.
    def wrapper(*args):
        nonlocal cache
        if args in cache:
            # Якщо результат є в кеші, повертаємо його.
            print("[CACHE] Повертаємо кешований результат")
            return cache[args]
        result = func(*args)
        cache[args] = result  # Зберігаємо результат у кеш.
        return result
    return wrapper

@simple_cache
def slow_func(x):
    # Функція, що симулює повільні обчислення.
    print("Обчислюємо результат... ")
    return x ** x

@simple_cache
def slow_func2(x):
    # Функція, що симулює затримку при обчисленні.
    for i in range(1, 5):
        print("Sleep")
        sleep(1)
    return 2 ** x

#############################################
# 13. Декоратор для перевірки прав доступу (require_admin)
#############################################
def require_admin(func):
    # Декоратор, що перевіряє, чи має користувач роль "admin".
    def wrapper(user, *args, **kwargs):
        if user.get("role") != "admin":
            # Якщо користувач не має ролі admin, викликаємо помилку.
            raise PermissionError("Доступ заборонено: тільки для адміна")
        return func(user, *args, **kwargs)
    return wrapper

@require_admin
def delete_user(user, user_id):
    # Функція для видалення користувача за заданим user_id.
    return f"User {user_id} delete"

#############################################
# 14. Декоратор з TTL (Time-to-Live) кешування
#############################################
import time

def ttl_cache(ttl):
    # Фабрика декораторів для TTL-кешування з заданим часом життя (ttl).
    cache = {}  # Словник для збереження кешованих результатів разом з часовими мітками.
    def decorator(func):
        nonlocal cache
        def wrapper(*args, **kwargs):
            nonlocal cache
            # Формуємо ключ з аргументів функції (args, kwargs).
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()  # Отримуємо поточний час.
            if key in cache:
                result, timestamp = cache[key]
                # Якщо з моменту збереження результату минуло менше, ніж ttl, повертаємо кеш.
                if current_time - timestamp < ttl:
                    print("[CACHE]")
                    return result
            # Якщо кеш відсутній або час життя вичерпано, викликаємо функцію.
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        return wrapper
    return decorator

@ttl_cache(ttl=5)
def get_data(x):
    # Функція, що симулює отримання даних.
    print("Result ...")
    return x * 10

#############################################
# 15. Декоратор для збору метрик викликів функції
#############################################
def metrics_collector(func):
    # Декоратор для збору метрик: кількості викликів та середнього часу виконання функції.
    call_count = 0  # Лічильник викликів.
    total_time = 0  # Сумарний час виконання функції.

    def wrapper(*args, **kwargs):
        nonlocal call_count, total_time
        start = time.time()  # Початок вимірювання часу.
        result = func(*args, **kwargs)
        end = time.time()  # Завершення вимірювання часу.
        call_count += 1
        total_time += (end - start)
        # Виводимо метрики: кількість викликів та середній час виконання.
        print(f"[METRICS] {func.__name__}: {call_count} викликів, середній час {total_time/call_count:.4f} сек")
        return result
    return wrapper

@metrics_collector
def process_request_metric(request):
    # Функція для симуляції обробки запиту з затримкою.
    time.sleep(0.5)
    return f"Processed {request}"

#############################################
# 16. Декоратор для валідації введених даних
#############################################
def validate_input(required_keys):
    # Фабрика декораторів для перевірки наявності обов'язкових ключів у даних.
    def decorator(func):
        def wrapper(data):
            # Перевіряємо, чи всі обов'язкові ключі присутні у даних.
            missing = [key for key in required_keys if key not in data]
            if missing:
                raise ValueError(f"Відсутні ключі: {missing}")
            return func(data)
        return wrapper
    return decorator

@validate_input(["username", "password"])
def register_user(data):
    # Функція для реєстрації користувача. Повертає повідомлення про успішну реєстрацію.
    return f"Користувача {data['username']} зареєстровано"

#############################################
# Основний блок виконання (if __name__ == '__main__')
#############################################
if __name__ == '__main__':
    # 1. Тест функції додавання чисел.
    print("1. Тест функції додавання чисел:")
    operation = add
    print(f"Result {operation(2, 3)}")  # Очікується: Result 5
    print()

    # 2. Тест обробки HTTP-запитів.
    print("2. Тест обробки HTTP-запитів (GET, POST, PUT):")
    print(process_request('GET', {}))     # Очікується: GET Response
    print(process_request('POST', {}))    # Очікується: POST Response
    print(process_request('PUT', {}))     # Очікується: 405 Method Not Allowed
    print()

    # 3. Тест фільтрації списку даних (залишаються лише додатні числа).
    print("3. Тест фільтрації списку даних:")
    numbers = [5, -3, 0, 10]
    print(process_list(numbers))  # Очікується: [5, 10]
    print()

    # 4. Тест обробки введених даних користувача (trim пробілів).
    print("4. Тест обробки введених даних користувача:")
    user_data = {'username': ' bob ', 'email': 'bob@example.com '}
    print(process_user_input(user_data))
    print()

    # 5. Тест застосування операції (віднімання).
    print("5. Тест застосування операції (віднімання):")
    print(apply_operation(10, 4, subtract))  # Очікується: 6
    print()

    # 6. Тест фільтрації записів (активних користувачів).
    print("6. Тест фільтрації записів (активних користувачів):")
    users = [
        {"id": 1, "name": "Bob", "active": True},
        {"id": 2, "name": "Alice", "active": False}
    ]
    active_users = filter_records(users, is_active_user)
    print(active_users)  # Очікується: список активних користувачів
    print()

    # 7. Тест функцій привітання.
    print("7. Тест функцій привітання:")
    say_hello = greeting_factory("Hello")
    say_how_are_you = greeting_factory("How are you?")
    print(say_hello("Bob"))
    print(say_how_are_you("Bob"))
    print(say_hello("Alice"))
    print(say_how_are_you("Alice"))
    print()

    # 8. Тест логування помилок (Logger 1).
    print("8. Тест логування помилок (Logger 1):")
    print(process_order({"amount": 10}))  # Очікується: Order processed
    print(process_order({"amount": -5}))  # Очікується: повідомлення про помилку
    print()

    # 9. Тест логування помилок (Logger 2).
    print("9. Тест логування помилок (Logger 2):")
    print(process_order_logger({"amount": 10}))  # Очікується: Order processed
    print(process_order_logger({"amount": -5}))  # Очікується: None (помилка залогована)
    print()

    # 10. Тест обробки замовлень з try/except.
    print("10. Тест обробки замовлень з try/except:")
    try:
        result = process_order1({"amount": 10})
        print(result)
        result2 = process_order1({"amount": -5})
        print(result2)
    except Exception as e:
        print(f"[ERROR] {e}")
    print()

    # 11. Тест декоратора rate_limited (обмеження викликів).
    print("11. Тест декоратора rate_limited:")
    print(api_request("/data"))    # Виклик 1
    print(api_request("/status"))  # Виклик 2
    print(api_request("/info"))    # Виклик 3
    try:
        print(api_request("/extra"))  # Виклик, що перевищує ліміт
    except Exception as e:
        print("Error 404")
    print()

    # 12. Тест кешування функцій (simple_cache).
    print("12. Тест кешування функцій (simple_cache):")
    print(slow_func2(100))
    print(slow_func2(1000))
    print(slow_func2(100))
    print(slow_func2(1000))
    print(slow_func2(10))
    print("Result", slow_func(4))
    print("Result", slow_func(5))
    print("Result", slow_func(5))
    print("Result", slow_func(4))
    print()

    # 13. Тест перевірки прав доступу (require_admin).
    print("13. Тест перевірки прав доступу (require_admin):")
    admin = {"name": "Alice", "role": "admin"}
    regular_user = {"name": "Bob", "role": "user"}
    print(f"Delete {delete_user(admin, 42)}")
    try:
        print(f"Delete {delete_user(regular_user, 42)}")
    except PermissionError as e:
        print("Error", e)
    print()

    # 14. Тест TTL-кешування (ttl_cache).
    print("14. Тест TTL-кешування (ttl_cache):")
    print(f"Result: {get_data(3)}")
    print("Waiting")
    time.sleep(3)
    print(f"Result: {get_data(3)}")
    print(f"Result: {get_data(3)}")
    print(f"Result: {get_data(3)}")
    print("Waiting")
    time.sleep(3)
    print(f"Result: {get_data(3)}")
    time.sleep(3)
    print(f"Result: {get_data(3)}")
    print()

    # 15. Тест збору метрик викликів функції (metrics_collector).
    print("15. Тест збору метрик викликів функції (metrics_collector):")
    print(process_request_metric("Request 1"))
    print(process_request_metric("Request 2"))
    print(process_request_metric("Request 3"))
    print()

    # 16. Тест валідації введених даних (validate_input).
    print("16. Тест валідації введених даних (validate_input):")
    print("Register:", register_user({"username": "alice", "password": "1234"}))
    try:
        print("Register:", register_user({"username": "bob"}))
    except ValueError as e:
        print("Error:", e)
