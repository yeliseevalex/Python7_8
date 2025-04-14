import pytest
import time

# Функція додавання
def add(x, y):
    return x + y

# Окремі тести
def test_add_positive_numbers():
    assert add(3, 5) == 8

def test_add_negative_numbers():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0

def test_add_mixed():
    assert add(-1, 1) == 0

# Параметризовані тести
@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),
    (-1, -2, -3),
    (0, 0, 0),
    (-1, 1, 0)
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected

# Фікстура, яка повертає список чисел
@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

# Тестуємо суму елементів списку
def test_sum(sample_list):
    assert sum(sample_list) == 15

# Тестуємо довжину списку
def test_len(sample_list):
    assert len(sample_list) == 5

# Функція калькулятора з різними операціями
def calc(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "sub":
        return a - b
    elif operation == "mul":
        return a * b
    elif operation == "div":
        if b == 0:
            raise ZeroDivisionError("Ділення на нуль")
        return a / b
    else:
        raise ValueError(f"Невідома {operation} операція")

# Параметризований тест калькулятора
@pytest.mark.parametrize("operation, a, b, expected", [
    ('add', 3, 5, 8),
    ('sub', 10, 4, 6),
    ('mul', 2, 3, 6),
    ('div', 8, 2, 4)
])
def test_calc(operation, a, b, expected):
    assert calc(operation, a, b) == expected

# Функція ділення з обробкою ділення на нуль
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Ділення на нуль")
    return a / b

# Успішне ділення
def test_divide_success():
    assert divide(10, 2) == 5

# Успішне ділення з негативним числом
def test_divide_success2():
    assert divide(-10, 2) == -5

# Перевірка винятку ділення на нуль
def test_divide_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Отримання поточного часу (мокаємо time.time)
def get_current_time():
    return time.time()

# Тест із monkeypatch для time.time
def test_get_current_time(monkeypatch):
    fixed_time = 1609459200  # 01.01.2021 00:00:00

    def fake_time():
        return fixed_time

    monkeypatch.setattr(time, "time", fake_time)

    assert get_current_time() == fixed_time

# Функція перетворення тексту у верхній регістр
def to_upper(text):
    return text.upper()

# Тест для функції to_upper
def test_to_upper():
    assert to_upper("python") == "PYTHON"

# Функція розділення тексту
def split_text(text, delimiter=" "):
    if not isinstance(delimiter, str):
        raise TypeError("Роздільник повинен бути рядком")
    return text.split(delimiter)

# Тест функції розділення
def test_split_text():
    text = "hello;world"
    assert split_text(text, ";") == ["hello", "world"]

# Тест обробки винятку при неправильному типі роздільника
def test_split_text_error():
    with pytest.raises(TypeError):
        split_text("hello world", 2)
