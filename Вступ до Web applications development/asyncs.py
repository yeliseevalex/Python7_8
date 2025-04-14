# Приклад завантаження файлів з використанням asyncio
import asyncio
import random
import time
import threading
import requests
import aiohttp
import multiprocessing

# Асинхронне завантаження файлу
async def download_file(name):
    print(f"Початок завантаження файлу {name}")
    await asyncio.sleep(1)
    return f"Завантажено файл {name}"

# Асинхронний запуск завантаження кількох файлів
async def download_main():
    tasks = [
        asyncio.create_task(download_file("file1")),
        asyncio.create_task(download_file("file2")),
        asyncio.create_task(download_file("file3"))
    ]
    results = await asyncio.gather(*tasks)
    print("Результати завантаження:", results)

# Приклад асинхронної задачі з випадковою затримкою
async def integral(name):
    delay = random.randint(1, 5)
    print(f"Затримка для {name} -> {delay}")
    await asyncio.sleep(delay)

async def slow_task(name):
    await integral(name)
    return f"{name} завершено"

# Обробка завдань по мірі їх завершення
async def slow_tasks_main():
    tasks = [slow_task(f'Task {i}') for i in range(5)]
    for finished in asyncio.as_completed(tasks):
        result = await finished
        print(result)

# Отримання даних з БД (імітація)
async def get_from_db(product_id):
    print(f"Шукаємо товар {product_id} в БД...")
    await asyncio.sleep(1.5)
    return {"id": product_id, "name": "Ноутбук", "stock": 7}

# Отримання ціни з зовнішнього API (імітація)
async def get_external_price(product_id):
    print(f"Отримуємо ціну з API для {product_id}...")
    await asyncio.sleep(1.0)
    return round(random.uniform(500,700))

# Обробка запиту користувача
async def handle_request(product_id):
    print(f"Обробляємо запит для товару {product_id}...")
    db_task = asyncio.create_task(get_from_db(product_id))
    price_task = asyncio.create_task(get_external_price(product_id))
    product_data = await db_task
    price = await price_task
    response = {
        "product": product_data["name"],
        "stock": product_data["stock"],
        "price_usd": price
    }
    print(f"Відповідь для користувача: {response}")

# Основна функція обробки запитів до товарів
async def handle_products_main():
    product_ids = [101, 102, 103]
    tasks = [handle_request(pid) for pid in product_ids]
    await asyncio.gather(*tasks)

# Перевірка користувача
async def check_user_login(username, password):
    print(f"Перевіряємо користувача {username}")
    await asyncio.sleep(1)
    return username == "admin" and password == "123"

# Контролер входу в систему
async def login_controller(username, password):
    is_valid = await check_user_login(username, password)
    if is_valid:
        print("OK")
    else:
        print("No")

# Симуляція чату між користувачами
async def receive_msg(user):
    await asyncio.sleep(random.uniform(0.5, 2))
    print(f"{user} надіслав повідомлення")

async def chat_simulation():
    users = ["Anna", "Ivan", "Bob"]
    await asyncio.gather(*(receive_msg(user) for user in users))

# Основна функція логіну і чату
async def login_and_chat_main():
    print("\n----Вхід у систему----")
    await login_controller("admin", "1234")
    await login_controller("admin", "123")

    print("\n----Чат----")
    await chat_simulation()

# Синхронне завантаження сторінок з використанням threading
urls = [
    "https://www.google.com",
    "https://www.example.com",
    "https://www.python.org"
]

def fetch(url):
    response = requests.get(url)
    print(f"[Threading] {url}: {len(response.content)} байт")

def threading_example():
    threads = []
    for url in urls:
        thread = threading.Thread(target=fetch, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Асинхронне завантаження сторінок через aiohttp
async def fetch_async(session, url):
    async with session.get(url) as response:
        content = await response.read()
        print(f"[Asyncio] {url}: {len(content)} байт")

async def aiohttp_example():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, url) for url in urls]
        await asyncio.gather(*tasks)

# Синхронна задача для потоків і процесів
def task(name):
    delay = random.randint(5, 10)
    print(f"{name} спить {delay} секунд...")
    time.sleep(delay)
    print(f"{name} завершено!")

# Приклад threading
def threading_demo():
    threads = []
    for i in range(5):
        t = threading.Thread(target=task, args=(f"Thread-{i}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Приклад asyncio
async def async_task(name):
    delay = random.randint(1,3)
    print(f"{name} спить {delay} секунд")
    await asyncio.sleep(delay)
    print(f"{name} завершено!")

async def asyncio_demo():
    tasks = [async_task(f"Async-{i}") for i in range(5)]
    await asyncio.gather(*tasks)

# Приклад multiprocessing
def multiprocessing_demo():
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=task, args=(f"Process-{i}",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

# Головний блок
if __name__ == "__main__":
    # Завантаження файлів
    asyncio.run(download_main())

    # Повільні задачі з випадковою затримкою
    asyncio.run(slow_tasks_main())

    # Обробка товарів з БД і API
    start = time.time()
    asyncio.run(handle_products_main())
    end = time.time()
    print(f"Загальний час: {end - start:.2f} секунд")

    # Логін та чат
    asyncio.run(login_and_chat_main())

    # Завантаження сторінок через threading
    start = time.time()
    threading_example()
    print(f"[Threading] Загальний час: {time.time() - start:.2f} секунд")

    # Завантаження сторінок через asyncio
    start = time.time()
    asyncio.run(aiohttp_example())
    print(f"[Asyncio] Загальний час: {time.time() - start:.2f} секунд")

    # Порівняння threading, asyncio, multiprocessing
    threading_demo()
    asyncio.run(asyncio_demo())
    multiprocessing_demo()