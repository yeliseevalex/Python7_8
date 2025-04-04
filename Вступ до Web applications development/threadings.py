"""
Цей файл демонструє різноманітні приклади роботи з потоками, синхронізацією, таймерами,
синхронізацією за допомогою Condition та блокування, а також симуляцію роботи з датчиками,
файловими операціями та проблемою «обідніх філософів».
"""

#############################################
# Імпорт необхідних модулів
#############################################
import os          # Модуль для роботи з операційною системою (наприклад, отримання кількості CPU)
import time        # Модуль для роботи з часом та затримками
import threading   # Модуль для створення та синхронізації потоків
import random      # Модуль для генерації випадкових чисел
import requests    # Модуль для HTTP-запитів (отримання даних з мережі)
import sqlite3     # Модуль для роботи з SQLite базою даних
import logging     # Модуль для логування
from http import HTTPStatus  # Стандартні HTTP статуси

#############################################
# 1. Отримання кількості CPU
#############################################
# Виводимо кількість процесорних ядер у системі.
print("Кількість CPU:", os.cpu_count())

#############################################
# 2. Послідовне виконання завдань із затримкою
#############################################
def task(id, delay):
    # Виводимо повідомлення про старт завдання з певним ідентифікатором.
    print(f"Starting task {id}")
    # Затримка на вказаний час (delay) секунд.
    time.sleep(delay)
    # Виводимо повідомлення про завершення завдання.
    print(f"Finished task {id}")

#############################################
# 3. Паралельне виконання завдань з використанням потоків
#############################################
def task_threaded(id, delay):
    # Функція, що виводить старт, робить затримку, і виводить завершення завдання.
    print(f"Start task {id}")
    time.sleep(delay)
    print(f"End task {id}")

def task_thread():
    # Функція для запуску декількох завдань у потоках.
    threads = []  # Список для зберігання об'єктів потоків.
    # Створюємо та запускаємо 3 потоки.
    for i in range(1, 4):
        thread = threading.Thread(target=task_threaded, args=(i, 2))
        threads.append(thread)  # Додаємо потік у список.
        thread.start()          # Запускаємо потік.
    # Чекаємо завершення кожного потоку.
    for thread in threads:
        thread.join()

#############################################
# 4. Завантаження даних з мережі паралельно
#############################################
def fetch_data(url):
    # Функція для завантаження даних з URL.
    print(f"Fetching data from {url}")
    response = requests.get(url)  # Виконуємо HTTP GET запит.
    # Виводимо розмір отриманого контенту (у байтах) разом із URL.
    print(f"{len(response.content)} bytes from {url}")

def fetch_data_thread(urls):
    # Функція для паралельного завантаження даних з кількох URL.
    threads = []  # Список для потоків.
    for url in urls:
        # Створюємо потік для кожного URL.
        thread = threading.Thread(target=fetch_data, args=(url,))
        threads.append(thread)
        thread.start()  # Запускаємо потік.
    # Чекаємо завершення всіх потоків.
    for thread in threads:
        thread.join()

# Список URL для завантаження даних.
urls = [
    "https://www.google.com",
    "https://www.example.com",
    "https://www.python.org",
    "https://www.example.com",
    "https://www.python.org",
    "https://www.google.com"
]

#############################################
# 5. Використання потоків з демонстрацією статусу (is_alive)
#############################################
def worker(name, delay):
    # Функція-робітник, що демонструє затримку роботи.
    print(f"{name} Started")
    time.sleep(delay)
    print(f"{name} Finished")

#############################################
# 6. Синхронізація потоків за допомогою threading.Event
#############################################
# Створюємо об'єкт події (Event) для синхронізації потоків.
start_event = threading.Event()

def wait_for_event(name):
    # Функція, що чекає встановлення події.
    print(f"{name} Waiting for event")
    start_event.wait()  # Чекаємо, поки подія не буде встановлена.
    print(f"{name} Event is set, processing")
    time.sleep(1)
    print(f"{name} Finished")

#############################################
# 7. Використання threading.Timer для затриманого виконання завдання
#############################################
def delayed_task():
    # Функція, що демонструє виконання завдання після затримки.
    print("Delayed task start!")

#############################################
# 8. Синхронізація потоків з використанням Condition (Producer/Consumer)
#############################################
condition = threading.Condition()  # Об'єкт Condition для координації потоків.
shared_data = []  # Глобальний список, що слугує спільним ресурсом.

def producer():
    global shared_data
    # Продуцент додає 5 випадкових чисел у список.
    for i in range(5):
        with condition:
            # Генеруємо випадкове число від 1 до 100.
            item = random.randint(1, 100)
            shared_data.append(item)
            print(f"Producer added {item}")
            condition.notify()  # Сповіщаємо споживача, що з'явився новий елемент.
            time.sleep(random.uniform(0.5, 1.5))
    with condition:
        # Додаємо спеціальний маркер (None) для сигналу завершення.
        shared_data.append(None)
        condition.notify()

def consumer():
    global shared_data
    # Споживач постійно обробляє елементи зі списку.
    while True:
        with condition:
            # Якщо список порожній, чекаємо на появу нових даних.
            while not shared_data:
                condition.wait()
            # Видаляємо перший елемент зі списку.
            item = shared_data.pop(0)
            if item is None:
                print("No more items!!!")
                break
            print(f"Get item - {item}")
            time.sleep(random.uniform(1, 2))

#############################################
# 9. Моделювання продажу квитків із використанням Lock
#############################################
tickets = 10  # Загальна кількість квитків.
lock = threading.Lock()  # Блокування для синхронізації доступу до змінної tickets.

def book_ticket(user):
    global tickets
    # Імітуємо затримку для імітації реальної роботи.
    time.sleep(random.uniform(0.1, 1.0))
    with lock:
        # Якщо ще є квитки, бронюємо один.
        if tickets > 0:
            print(f"{user} booked a ticket. Tickets left: {tickets - 1}")
            tickets -= 1
        else:
            print(f"{user} tried to book a ticket but sold out")

def user_thread(user):
    # Потік для одного користувача, що намагається забронювати квиток.
    while True:
        with lock:
            if tickets <= 0:
                break
        book_ticket(user)
        time.sleep(random.uniform(0.1, 0.5))

#############################################
# 10. Проблема «обідніх філософів»
#############################################
class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork):
        # Ініціалізуємо потік-філософа з ім'ям та двома виделками.
        super().__init__()
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.running = True  # Прапорець, що контролює роботу потоку.

    def run(self):
        # Основний цикл роботи філософа.
        while self.running:
            print(f"{self.name} is thinking")
            time.sleep(random.uniform(0.5, 2))
            print(f"{self.name} is hungry")
            with self.left_fork:
                print(f"{self.name} picked up left fork")
                with self.right_fork:
                    print(f"{self.name} picked up right fork and is eating")
                    time.sleep(random.uniform(0.5, 1.5))
                    print(f"{self.name} finished eating and put down forks")

#############################################
# 11. Симуляція зчитування даних з сенсора за допомогою Timer
#############################################
def read_sensor():
    # Зчитуємо випадкове значення з сенсора та виводимо його разом із поточним часом.
    sensor_value = random.uniform(20.0, 30.0)
    print(f"Sensor reading: {sensor_value:.2f}C as {time.strftime('%H:%M:%S')}")
    # Створюємо таймер, який повторно викличе read_sensor через 4 секунди.
    timer = threading.Timer(4.0, read_sensor)
    timer.daemon = True  # Робимо таймер демон-потоком.
    timer.start()

#############################################
# 12. Читання файлу та обробка даних з використанням Condition
#############################################
condition_file = threading.Condition()  # Створюємо об'єкт Condition для синхронізації.
file_data = None  # Глобальна змінна для зберігання даних, зчитаних з файлу.

def file_reader():
    global file_data
    # Імітуємо затримку читання файлу.
    time.sleep(random.uniform(1, 2))
    with condition_file:
        file_data = "Data from file"  # Імітуємо отримані дані з файлу.
        print("File reader: Data is read and available.")
        condition_file.notify()  # Сповіщаємо, що дані готові.

def data_processor():
    global file_data
    with condition_file:
        # Якщо дані ще не доступні, чекаємо.
        while file_data is None:
            print("Data processor: Waiting for data...")
            condition_file.wait()
        # Виводимо повідомлення про обробку отриманих даних.
        print(f"Data processor: Processing '{file_data}'")
    time.sleep(1)  # Імітуємо затримку обробки.
    print("Data processor: Finished processing.")

#############################################
# Основний блок виконання
#############################################
if __name__ == '__main__':
    print("\n=== Початок демонстрації роботи потоків та синхронізації ===\n")

    #########################################
    # 2. Послідовне виконання завдань із затримкою
    #########################################
    print("2. Послідовне виконання завдань:")
    start = time.time()
    task(1, 2)
    task(2, 2)
    task(3, 2)
    end = time.time()
    print(f"Total time {end - start:.2f} seconds\n")

    #########################################
    # 3. Паралельне виконання завдань з використанням потоків
    #########################################
    print("3. Паралельне виконання завдань з потоками:")
    start = time.time()
    task_thread()
    end = time.time()
    print(f"Total time {end - start:.2f} seconds\n")

    #########################################
    # 4. Завантаження даних з мережі паралельно
    #########################################
    print("4. Завантаження даних з мережі:")
    fetch_data_thread(urls)
    print()

    #########################################
    # 5. Демонстрація статусу потоків (is_alive)
    #########################################
    print("5. Демонстрація статусу потоків:")
    thread1 = threading.Thread(target=worker, args=("Thread-1", 2))
    thread2 = threading.Thread(target=worker, args=("Thread-2", 5))
    thread2.daemon = True  # Встановлюємо, що Thread-2 є демон-потоком.
    thread1.start()
    thread2.start()
    print(f"is alive 1? {thread1.is_alive()}")
    print(f"is alive 2? {thread2.is_alive()}")
    thread1.join()
    print(f"Is Thread-2 still alive? {thread2.is_alive()}")
    print("Main thread finished\n")

    #########################################
    # 6. Синхронізація потоків з використанням Event
    #########################################
    print("6. Синхронізація потоків за допомогою Event:")
    threads_event = []
    for i in range(3):
        t = threading.Thread(target=wait_for_event, args=(f"Thread-{i+1}",))
        threads_event.append(t)
        t.start()
    time.sleep(2)
    print("Setting event now")
    start_event.set()  # Встановлюємо подію, щоб потоки могли продовжити роботу.
    for t in threads_event:
        t.join()
    print("All threads have finished\n")

    #########################################
    # 7. Використання Timer для затриманого виконання завдання
    #########################################
    print("7. Використання Timer:")
    timer = threading.Timer(5.0, delayed_task)
    print("Timer start, task will start after 5 seconds")
    timer.start()
    timer.cancel()  # Скасовуємо таймер.
    delayed_task()  # Викликаємо завдання вручну.
    print()

    #########################################
    # 8. Синхронізація потоків (Producer/Consumer) за допомогою Condition
    #########################################
    print("8. Producer/Consumer з Condition:")
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()
    print("Finished...\n")

    #########################################
    # 9. Моделювання продажу квитків із використанням Lock
    #########################################
    print("9. Моделювання продажу квитків:")
    tickets = 10  # Скидаємо кількість квитків для демонстрації.
    threads_ticket = []
    for i in range(15):
        t = threading.Thread(target=user_thread, args=(f"User-{i+1}",))
        threads_ticket.append(t)
        t.start()
    for t in threads_ticket:
        t.join()
    print("Tickets sold out!!!\n")

    #########################################
    # 10. Проблема «обідніх філософів»
    #########################################
    print("10. Проблема «обідніх філософів»:")
    forks = [threading.Lock() for _ in range(5)]
    names = ["PH-1", "PH-2", "PH-3", "PH-4", "PH-5"]
    philosophers = []
    for i in range(5):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % 5]
        p = Philosopher(names[i], left_fork, right_fork)
        philosophers.append(p)
        p.start()
    time.sleep(5)
    for p in philosophers:
        p.running = False
    print()
    time.sleep(2)
    print()

    #########################################
    # 11. Симуляція зчитування даних з сенсора за допомогою Timer
    #########################################
    print("11. Симуляція даних з сенсора:")
    print("Starting sensor data simulation")
    initial_timer = threading.Timer(4.0, read_sensor)
    initial_timer.start()
    for i in range(5):
        print(f"Main application working... {i+1}")
        time.sleep(3)
    time.sleep(10)
    print()

    #########################################
    # 12. Читання файлу та обробка даних з використанням Condition
    #########################################
    print("12. Читання файлу та обробка даних з Condition:")
    reader_thread = threading.Thread(target=file_reader)
    processor_thread = threading.Thread(target=data_processor)
    reader_thread.start()
    processor_thread.start()
    reader_thread.join()
    processor_thread.join()
    print("File processing simulation finished.\n")

    print("=== Кінець демонстрації роботи потоків та синхронізації ===\n")
