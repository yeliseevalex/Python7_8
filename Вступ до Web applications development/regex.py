#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Урок з регулярних виразів (Regex) для Python
Цей файл містить приклади використання модуля re.
Приклади охоплюють базовий синтаксис, квантори, символьні класи, групування, а також функції re.search, re.match, re.findall, re.sub, re.split, re.compile і використання прапорців.
"""

import re

# 1. Базові символи: крапка (.)
def example_dot():
    print("--- 2.1: Базові символи: Крапка (.) ---")
    text = "abc\ndef"  # Текст з двома рядками
    pattern = r"a."    # Шаблон: літера 'a' та будь-який символ (крім символу нового рядка)
    print("Результат (працює):", re.findall(pattern, text))  # Очікується ['ab']

    text2 = "a\nb"  # Символ нового рядка розділяє 'a' та 'b'
    print("Результат (не спрацює):", re.findall(pattern, text2))  # Порожній список через відсутність збігу

# 2. Квантори (повторення)
def example_quantifiers():
    print("\n--- 2.2: Квантори (повторення) ---")
    # Квантор *
    text = "ab, a, abb"
    pattern = r"ab*"  # 'a' з 0 або більше 'b'
    print("ab*:", re.findall(pattern, text))  # ['ab', 'a', 'abb']

    # Квантор +
    text = "a ab abb abbb"
    pattern = r"ab+"  # 'a' з 1 або більше 'b'
    print("ab+:", re.findall(pattern, text))  # ['ab', 'abb', 'abbb']

    # Квантор ?
    text = "colouor color"
    pattern = r"colou?r"  # Літера 'u' може бути або бути відсутньою
    print("colou?r:", re.findall(pattern, text))  # ['colouor', 'color']

    # Фігурні дужки {n}, {n,}, {n,m}
    pattern = r"\d{3}"  # Рівно 3 цифри
    print("Рівно 3 цифри:", re.findall(pattern, "123 45 6789"))  # ['123']

    pattern = r"\d{2,}"  # 2 або більше цифр
    print("2 або більше цифр:", re.findall(pattern, "5 12 123 1"))  # ['12', '123']

    pattern = r"\d{2,4}"  # Від 2 до 4 цифр
    print("Від 2 до 4 цифр:", re.findall(pattern, "1 12 123 12345"))  # ['12', '123']

    # Приклад з повторенням, де може залишитись символ:
    text = "aaaaa"
    pattern = r"a{2,4}"
    print("a{2,4} для 'aaaaa':", re.findall(pattern, text))
    # Зауваження: регулярні вирази повертають неперекривні збіги, тому остання 'a' може не бути захоплена.

# 3. Символьні класи та спеціальні символи
def example_char_classes():
    print("\n--- 2.3: Символьні класи та спеціальні символи ---")
    text = "abcde"
    pattern = r"[abc]"  # Будь-який символ з 'a', 'b', 'c'
    print("Символьний клас [abc]:", re.findall(pattern, text))  # ['a', 'b', 'c']

    pattern = r"[^ab]"  # Будь-який символ, окрім 'a' та 'b'
    print("Заперечення [^ab]:", re.findall(pattern, text))  # ['c', 'd', 'e']

    text = "abc 123 _-!"
    print("Цифри:", re.findall(r"\d", text))      # ['1', '2', '3']
    print("Символи \\w:", re.findall(r"\w", text))  # ['a', 'b', 'c', '1', '2', '3', '_']
    print("Пробіли:", re.findall(r"\s", text))      # [' ']

# 4. Групування та альтернативи
def example_grouping_alternation():
    print("\n--- 2.4: Групування та альтернативи ---")
    # Групування для вилучення підрядків
    text = "gray, grey"
    pattern = r"gr(a|e)y"  # Група з вибором 'a' або 'e'
    print("gr(a|e)y:", re.findall(pattern, text))  # ['a', 'e']

    text = "gray, grey"
    pattern = r"gr(?:a|e)y" # Група з вибором 'gray' або 'grey'
    print(re.findall(pattern, text)) # ['gray', 'grey']

    text = "Дата: 2025-03-28"
    pattern = r"(\d{4})-(\d{2})-(\d{2})"  # Групи для року, місяця та дня
    match = re.search(pattern, text)
    if match:
        year, month, day = match.groups()
        print("Групування:", "Рік:", year, "Місяць:", month, "День:", day)

    # Альтернатива
    text = "cat dog mouse"
    pattern = r"cat|mouse"
    print("Альтернатива:", re.findall(pattern, text))  # ['cat', 'mouse']

    text = "gray, grey, grxy"
    pattern = r"gr(a|e|x)y"
    print("gr(a|e|x)y:", re.findall(pattern, text))  # ['a', 'e', 'x']

# 5. Функція re.search()
def example_re_search():
    print("\n--- 3.1: re.search() ---")
    text = "Координати: 12.34, 56.78"
    pattern = r"(\d+\.\d+),\s*(\d+\.\d+)"
    match = re.search(pattern, text)
    if match:
        lat, lon = match.groups()
        print("re.search (працює):", "Широта:", lat, "Довгота:", lon)

    # Приклад з потенційною проблемою (екранування коми)
    text = "Координати: 12.34, 56.78"
    pattern = r"(\d+\.\d+)\,\s*(\d+\.\d+)"
    match = re.search(pattern, text)
    if match:
        print("re.search (з потенційною проблемою):", match.groups())
    else:
        print("Шаблон не знайшов збіг")

# 6. Функція re.match()
def example_re_match():
    print("\n--- 3.2: re.match() ---")
    text = "Python - це чудово!"
    pattern = r"Python"  # Шаблон перевіряє початок рядка
    if re.match(pattern, text):
        print("re.match (працює): Рядок починається з 'Python'")

    text = "Вчимо Python"
    pattern = r"Python"
    if re.match(pattern, text):
        print("Рядок починається з 'Python'")
    else:
        print("re.match: Збіг не знайдено, бо 'Python' не на початку")

# 7. Функції re.findall() та re.finditer()
def example_re_findall_finditer():
    print("\n--- 3.3: re.findall() та re.finditer() ---")
    text = "У тексті є 3 числа: 12, 345 та 67."
    pattern = r"\d+"
    print("re.findall():", re.findall(pattern, text))  # Знаходить всі послідовності цифр

    text = "1111"
    pattern = r"11"  # Неперекривні збіги
    print("Перекривання:", re.findall(pattern, text))  # ['11', '11']

# 8. Функція re.sub()
def example_re_sub():
    print("\n--- 3.4: re.sub() ---")
    text = "Я люблю Python!"
    pattern = r"Python"
    print("re.sub (працює):", re.sub(pattern, "Regex", text))

    text = "Це текст з   декількома  пробілами\nі новими рядками."
    pattern = r" "  # Замінить лише окремі пробіли
    print("re.sub (проблемний шаблон):", re.sub(pattern, "-", text))
    # Порада: для заміни усіх послідовностей пробілів використовувати r"\s+"

# 9. Функція re.split()
def example_re_split():
    print("\n--- 3.5: re.split() ---")
    text = "яблуко, банан; апельсин. Груша"
    pattern = r"[,\.;]\s*"  # Розбиваємо за комами, крапками з комою або крапками з опціональним пробілом
    print("re.split (працює):", re.split(pattern, text))

    text = "яблуко,банан;апельсин.Груша"
    pattern = r"[,\.;] "  # Очікує, що після роздільника завжди буде пробіл
    print("re.split (проблемний шаблон):", re.split(pattern, text))

# 10. Функція re.compile()
def example_re_compile():
    print("\n--- 3.6: re.compile() ---")
    pattern = re.compile(r"\d+")
    text = "Числа: 10, 20, 30"
    print("re.compile:", pattern.findall(text))

# 11. Використання прапорців
def example_flags_ignorecase():
    print("\n--- 4.1: re.IGNORECASE ---")
    text = "Hello\nhello\nHELLO"
    pattern = r"hello"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    print("IGNORECASE:", matches)

def example_flags_multiline():
    print("\n--- 4.2: re.MULTILINE ---")
    text = "Перший рядок\nДругий рядок"
    pattern = r"^\w+"  # Початкове слово кожного рядка
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    print("MULTILINE:", matches)
    matches = re.findall(pattern, text)
    print("Без MULTILINE:", matches)

def example_flags_dotall():
    print("\n--- 4.3: re.DOTALL ---")
    text = "Перший рядок\nДругий рядок"
    pattern = r".+"
    match = re.search(pattern, text, flags=re.DOTALL)
    if match:
        print("DOTALL:", match.group())
    match = re.search(pattern, text)
    if match:
        print("Без DOTALL:", match.group())

def example_flags_verbose():
    print("\n--- 4.4: re.VERBOSE ---")
    pattern_verbose = re.compile(r"""
        ^                   # Початок рядка
        (?P<area_code>\d{3})   # Код області (3 цифри)
        [\s-]?              # Опціональний пробіл або тире
        (?P<number>\d{3}-\d{4}) # Основний номер, наприклад 456-7890
        $                   # Кінець рядка
        """, re.VERBOSE)
    text = "123-456-7890"
    match = pattern_verbose.search(text)
    if match:
        print("VERBOSE:", "Код:", match.group("area_code"), "Номер:", match.group("number"))

    # Приклад без re.VERBOSE (може бути проблема через пробіли та коментарі)
    pattern_nonverbose = r"""
        \d{3}    # код області
        \s*      # пробіли
        \d{3}-\d{4}
        """
    match = re.search(pattern_nonverbose, "123 456-7890")
    print("Без VERBOSE:", match)

# 12. Приклади застосувань у реальних завданнях
## 12.1. Перевірка електронної адреси
def example_email_validation():
    print("\n--- 5.1: Перевірка електронної адреси ---")
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    emails = [
        "example@mail.com",
        "user.name+tag+sorting@example.com",
        "test.email@sub.example.co.uk"
    ]
    for email in emails:
        if re.match(pattern, email):
            print(f"{email} - коректна адреса")
        else:
            print(f"{email} - некоректна адреса")

    # Приклад з надто суворим шаблоном
    pattern_strict = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    emails = ["user@localhost", "name@example", "valid.email@example.com"]
    for email in emails:
        if re.match(pattern_strict, email):
            print(f"{email} - коректна адреса")
        else:
            print(f"{email} - некоректна адреса")

## 12.2. Витягування номерів телефону
def example_phone_numbers():
    print("\n--- 5.2: Витягування номерів телефону ---")
    text = "Контакти: +38 (067) 123-45-67, +38-099-765-43-21, 0671234567"
    pattern = r"(\+38[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2})|(\d{10})"
    phones = re.findall(pattern, text)
    phones_clean = [phone[0] if phone[0] else phone[1] for phone in phones]
    print("Номери телефонів (працює):", phones_clean)

    text = "Контакти: +380671234567, 067-123-45-67, 1234567890"
    pattern = r"\+38\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    phones = re.findall(pattern, text)
    print("Номери телефонів (проблемний шаблон):", phones)

## 12.3. Витягування URL-адрес із тексту
def example_extract_urls():
    print("\n--- 5.3: Витягування URL-адрес із тексту ---")
    text = "Відвідайте наш сайт: https://www.example.com або http://site.org для деталей."
    pattern = r"https?://(?:www\.)?\S+"
    urls = re.findall(pattern, text)
    print("URL-адреси (працює):", urls)

    text = "Перейдіть за посиланням: https://www.example.com. Або зайдіть на http://site.org!"
    pattern = r"https?://(?:www\.)?\S+"
    urls = re.findall(pattern, text)
    print("URL-адреси (з зайвими символами):", urls)

## 12.4. Розбиття тексту за роздільниками
def example_split_text():
    print("\n--- 5.4: Розбиття тексту за роздільниками ---")
    text = "яблуко, банан; апельсин. Груша"
    pattern = r"[,\.;]\s*"
    fragments = re.split(pattern, text)
    print("Розбитий текст (працює):", fragments)

    text = "яблуко,банан;апельсин.Груша"
    pattern = r"[,\.;] "  # Проблемний шаблон: очікує пробіл після роздільника
    print("Розбиття (проблемний шаблон):", re.split(pattern, text))

## 12.5. Використання іменованих груп для вилучення даних
def example_named_groups():
    print("\n--- 5.5: Використання іменованих груп для вилучення даних ---")
    text = "Користувач: john_doe, Email: john@example.com, Телефон: +38-067-123-45-67"
    pattern = r"Користувач:\s(?P<username>\w+),\sEmail:\s(?P<email>[\w\.-]+@[\w\.-]+),\sТелефон:\s(?P<phone>\+?\d[\d\-\s\(\)]{9,}\d)"
    match = re.search(pattern, text)
    if match:
        print("Іменовані групи:")
        print("  Username:", match.group("username"))
        print("  Email:", match.group("email"))
        print("  Phone:", match.group("phone"))

# 13. Використання re для складних завдань
## 13.1. Комплексна обробка тексту
def example_complex_text():
    print("\n--- 6.1: Комплексна обробка тексту ---")
    text = "Apple, banana, grape, orange, pear, peach, cherry, lemon"
    pattern = re.compile(r"\b\w*[ae]\w*\b", re.IGNORECASE)
    matches = pattern.finditer(text)
    words = [match.group() for match in matches]
    print("Слова, що містять 'a' або 'e':", words)
    print("Кількість знайдених слів:", len(words))

## 13.2. Використання re.VERBOSE для складних шаблонів (розбір номера телефону)
def example_verbose_phone():
    print("\n--- 6.2: Використання re.VERBOSE для складних шаблонів ---")
    pattern = re.compile(r"""
        ^                           # Початок рядка
        (?P<country>\+\d{1,3})?      # Код країни (опціонально): '+' та від 1 до 3 цифр
        [\s-]*                      # Опціональні пробіли або тире
        \(?(?P<area>\d{3})\)?       # Код області: 3 цифри, опціонально в дужках
        [\s-]*                      # Опціональні пробіли або тире
        (?P<number>\d{3}[-\s]?\d{2}[-\s]?\d{2})  # Основний номер з тире або пробілами
        $                           # Кінець рядка
        """, re.VERBOSE)
    samples = [
        "+38 (067) 123-45-67",
        "0671234567",
        "+380671234567"
    ]
    for sample in samples:
        m = pattern.search(sample)
        if m:
            print(f"Обробка для: {sample}")
            print("  Код країни:", m.group("country"))
            print("  Код області:", m.group("area"))
            print("  Номер:", m.group("number"))
        else:
            print(f"Шаблон не співпадає з: {sample}")

# 14. Розбір електронної адреси із використанням re.VERBOSE
def example_verbose_email():
    print("\n--- 8: Розбір електронної адреси із re.VERBOSE ---")
    pattern = re.compile(r"""
        ^                                # Початок рядка
        (?P<username>[a-zA-Z0-9_.+-]+)    # Ім'я користувача: дозволені літери, цифри, '_', '.', '+', '-'
        @                                # Символ '@'
        (?P<domain>[a-zA-Z0-9-]+)         # Домен: літери, цифри, тире
        \.                               # Точка як роздільник
        (?P<tld>[a-zA-Z]{2,})             # Доменне розширення (TLD): мінімум 2 літери
        $                                # Кінець рядка
        """, re.VERBOSE)
    samples = [
        "user@example.com",
        "john.doe+test@mail.com",
        "invalid-email",          # Некоректний email – шаблон не співпаде
        "another.user@domain.org"
    ]
    for sample in samples:
        m = pattern.search(sample)
        if m:
            print(f"Обробка для: {sample}")
            print("  Ім'я користувача:", m.group("username"))
            print("  Домен:", m.group("domain"))
            print("  TLD:", m.group("tld"))
        else:
            print(f"Шаблон не співпадає з: {sample}")

if __name__ == '__main__':
    example_dot()
    example_quantifiers()
    example_char_classes()
    example_grouping_alternation()
    example_re_search()
    example_re_match()
    example_re_findall_finditer()
    example_re_sub()
    example_re_split()
    example_re_compile()
    example_flags_ignorecase()
    example_flags_multiline()
    example_flags_dotall()
    example_flags_verbose()
    example_email_validation()
    example_phone_numbers()
    example_extract_urls()
    example_split_text()
    example_named_groups()
    example_complex_text()
    example_verbose_phone()
    example_verbose_email()
