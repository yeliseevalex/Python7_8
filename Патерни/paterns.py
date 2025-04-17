import threading
from abc import ABC, abstractmethod

# 1. Singleton (Одинак)
# Що це таке?
# Шаблон Singleton гарантує, що з одного класу буде створено лише один екземпляр.
# Інакше кажучи, протягом роботи програми завжди існує тільки один об’єкт цього класу.

# Приклад з життя:
# Уяви, що в місті є лише одна мерія. Кожен громадянин, якому потрібна
# довідка або консультація, звертається саме туди, бо альтернативи немає.
# Так само і в програмуванні: якщо потрібен єдиний об’єкт для управління
# (наприклад, з’єднання з базою даних), його реалізують через Singleton,
# щоб уникнути дублікатів, які можуть призвести до помилок.

# Простими словами:
# Навіщо: Щоб у системі не з’явилося кілька однакових «центральних» об’єктів.
# Як працює: Перед створенням нового об’єкта перевіряється, чи вже існує такий.
# Якщо так — повертається існуючий, інакше — створюється новий.

class CityHall:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Якщо об'єкта ще немає, створюємо його
        if cls._instance is None:
            print("Створюємо єдину мерію міста.")
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def serve_citizen(self, citizen_name):
        print(f"Мерія обслуговує громадянина {citizen_name}.")

hall1 = CityHall()
hall2 = CityHall()

print("hall1 is hall2:", hall1 is hall2)

hall1.serve_citizen("Олег")

# -----------------

class DBConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.connect()
            return cls._instance

    def connect(self):
        self.connection = "Підключення до бази даних встановлено"

db1 = DBConnection()
db2 = DBConnection()
print(db1 is db2)


# 2. Factory Method (Фабричний метод)
# Що це таке?
# Цей шаблон допомагає створювати об’єкти певного типу, але залишає вибір
# конкретного виду на пізніший етап. Тобто створення об’єкта не прив’язане
# жорстко до конкретного класу.

# Приклад з життя:
# Уяви фабрику іграшок. Коли надходить замовлення, менеджер вирішує, яку
# саме іграшку виробляти: м’ячик, ведмедика чи машинку. Все виробляється на
# одному заводі, але кінцевий продукт залежить від замовлення.

# Простими словами:
# Навіщо: Щоб не переписувати всю систему при появі нових типів об’єктів.
# Як працює: Є загальний інтерфейс, а конкретні реалізації визначаються в підкласах.

class Toy(ABC):
    @abstractmethod
    def play(self):
        pass

class Ball(Toy):
    def play(self):
        print("Граємо в мяч!")

class TeddyBear(Toy):
    def play(self):
        print("Обіймаємо плюшевого ведмедика!")

class Car(Toy):
    def play(self):
        print("Граємо з іграшковою машинкою!")

class ToyFactory(ABC):
    @abstractmethod
    def create_toy(self) -> Toy:
        pass

class BallFactory(ToyFactory):
    def create_toy(self) -> Toy:
        return Ball()

class TeddyBearFactory(ToyFactory):
    def create_toy(self) -> Toy:
        return TeddyBear()

class CarFactory(ToyFactory):
    def create_toy(self) -> Toy:
        return Car()

def produce_toy(factory: ToyFactory):
    toy = factory.create_toy()
    toy.play()

# Тестування:
produce_toy(BallFactory())
produce_toy(TeddyBearFactory())
produce_toy(CarFactory())


# -----------------

class Notification:
    def send(self, message):
        raise NotImplementedError

class EmailNotification(Notification):
    def send(self, message):
        print(f"[Email] {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"[SMS] {message}")

class PushNotification(Notification):
    def send(self, message):
        print(f"[Push] {message}")

class NotificationFactory:
    @staticmethod
    def create_notification(method):
        if method == "email":
            return EmailNotification()
        elif method == "sms":
            return SMSNotification()
        elif method == "push":
            return PushNotification()

notifier = NotificationFactory.create_notification("email")
notifier.send("Ваша заявка прийнята")


# 3. Observer (Спостерігач)
# Що це таке?
# Дозволяє одному об’єкту повідомляти інші об’єкти про зміни. Коли змінюється
# стан суб’єкта, всі підписники дізнаються про це автоматично.

# Приклад з життя:
# У соціальних мережах, коли хтось публікує пост — усі підписники отримують сповіщення.
#
# Простими словами:
# Навіщо: Щоб автоматично сповіщати об’єкти про зміни без опитування.
# Як працює: Суб’єкт зберігає список спостерігачів і повідомляє їх при зміні стану.

class SocialMediaAccount:
    def __init__(self, username):
        self.username = username
        self.followers = []

    def subscribe(self, observer):
        self.followers.append(observer)

    def unsubscribe(self, observer):
        self.followers.remove(observer)

    def new_post(self, content):
        print(f"{self.username} опублікував(ла) новий пост: {content}")
        self.notify_followers(content)

    def notify_followers(self, content):
        for follower in self.followers:
            follower.update(self, content)

class Follower:
    def __init__(self, name):
        self.name = name

    def update(self, account, content):
        print(f"{self.name} отримав(ла) сповіщення: {account.username} - {content}")

# Тестування:
account = SocialMediaAccount("Petya")
follower1 = Follower("Ivan")
follower2 = Follower("Olga")

account.subscribe(follower1)
account.subscribe(follower2)

account.new_post("Привіт, світ!")


# -----------------

class Order:
    def __init__(self):
        self._observers = []
        self.status = "нове"

    def attach(self, observer):
        self._observers.append(observer)

    def set_status(self, new_status):
        self.status = new_status
        self.notify_all()

    def notify_all(self):
        for obs in self._observers:
            obs.update(self.status)

class EmailObserver:
    def update(self, status):
        print(f"Email: Статус замовлення змінено на '{status}'")

order = Order()
order.attach(EmailObserver())
order.set_status("в обробці")

# 4. Decorator (Декоратор)
# Що це таке?
# Дозволяє динамічно додавати нову функціональність об’єкту, не змінюючи його структуру.

# Приклад з життя:
# Базова чашка кави — а ти можеш додати молоко, цукор, сироп. Кава та ж, але з новими смаками.

# Простими словами:
# Навіщо: Щоб додати нову функціональність без зміни вихідного коду.
# Як працює: Об’єкт обгортається в інший, який додає додаткові властивості чи поведінку.
class Coffee(ABC):
    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

class SimpleCoffee(Coffee):
    def get_cost(self):
        return 50

    def get_description(self):
        return "Проста кава"

class CoffeeDecorator(Coffee):
    def __init__(self, decorated_coffee: Coffee):
        self.decorated_coffee = decorated_coffee

    def get_cost(self):
        return self.decorated_coffee.get_cost()

    def get_description(self):
        return self.decorated_coffee.get_description()

class MilkDecorator(CoffeeDecorator):
    def get_cost(self):
        return self.decorated_coffee.get_cost() + 10

    def get_description(self):
        return self.decorated_coffee.get_description() + ", з додаванням молока"

class SugarDecorator(CoffeeDecorator):
    def get_cost(self):
        return self.decorated_coffee.get_cost() + 5

    def get_description(self):
        return self.decorated_coffee.get_description() + ", з додаванням цукру"

basic_coffee = SimpleCoffee()
print(basic_coffee.get_description(), "вартість:", basic_coffee.get_cost())

coffee_with_milk = MilkDecorator(basic_coffee)
print(coffee_with_milk.get_description(), "вартість:", coffee_with_milk.get_cost())

coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)
print(coffee_with_milk_and_sugar.get_description(), "вартість:", coffee_with_milk_and_sugar.get_cost())

# -----------------

from functools import wraps

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[LOG] Запит отримано")
        return func(*args, **kwargs)
    return wrapper

def check_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("[AUTH] Перевірка токену пройдена")
        return func(*args, **kwargs)
    return wrapper

@log_request
@check_auth
def handle_request():
    print("[HANDLER] Обробка запиту")

handle_request()

# 5. Adapter (Адаптер)
# Що це таке?
# Дозволяє об’єктам із несумісними інтерфейсами працювати разом.

# Приклад з життя:
# У тебе є стара розетка і новий електроприлад — адаптер дозволяє підключити одне до іншого.

# Простими словами:
# Навіщо: Щоб з’єднати несумісні об’єкти.
# Як працює: Адаптер перетворює інтерфейс одного об’єкта у формат, зрозумілий іншому.

class ExternalDevice:
    def plug_in(self):
        print("Пристрій підключено за допомогою методу plug_in.")

class DeviceInterface:
    def connect(self):
        raise NotImplementedError

class DeviceAdapter(DeviceInterface):
    def __init__(self, external_device: ExternalDevice):
        self.external_device = external_device

    def connect(self):
        self.external_device.plug_in()

external_device = ExternalDevice()
adapter = DeviceAdapter(external_device)
adapter.connect()

# -----------------

class ExternalCurrencyAPI:
    def get_rate(self):
        return {"usd": 38.1, "eur": 41.5}  # Умовний формат

class CurrencyAdapter:
    def __init__(self, api):
        self.api = api

    def get_usd_rate(self):
        return self.api.get_rate()["usd"]

api = ExternalCurrencyAPI()
adapter = CurrencyAdapter(api)
print(f"Курс USD: {adapter.get_usd_rate()}")

# 6. Strategy (Стратегія)
# Що це таке?
# Визначає сімейство алгоритмів і дозволяє вибрати один із них під час виконання програми.

# Приклад з життя:
# Ти їдеш на роботу: можеш вибрати головну дорогу або об’їзну — рішення залежить від трафіку.

# Простими словами:
# Навіщо: Щоб змінювати алгоритм «на льоту», не змінюючи сам об’єкт.
# Як працює: Є загальний інтерфейс, і кілька реалізацій, які можна підставляти за потреби.
class RouteStrategy(ABC):
    @abstractmethod
    def get_route(self, start, end):
        pass

class FastRoute(RouteStrategy):
    def get_route(self, start, end):
        return f"Швидкий маршрут від {start} до {end} по автомагістралі."

class ScenicRoute(RouteStrategy):
    def get_route(self, start, end):
        return f"Живописний маршрут від {start} до {end} через мальовничі місцевості."

class Navigator:
    def __init__(self, strategy: RouteStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: RouteStrategy):
        self.strategy = strategy

    def navigate(self, start, end):
        route = self.strategy.get_route(start, end)
        print(route)

navigator = Navigator(FastRoute())
navigator.navigate("Дніпро", "Київ")

navigator.set_strategy(ScenicRoute())
navigator.navigate("Дніпро", "Київ")

# -----------------

class DiscountStrategy:
    def apply(self, price):
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, price):
        return price

class TenPercentDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.9

class LoyalCustomerDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.8

class Order:
    def __init__(self, price, strategy):
        self.price = price
        self.strategy = strategy

    def final_price(self):
        return self.strategy.apply(self.price)

order = Order(1000, TenPercentDiscount())
print(f"Ціна зі знижкою: {order.final_price()}")

# 7. Command (Команда)
# Що це таке?
# Інкапсулює дію у вигляді об’єкта. Це дозволяє зберігати історію, реалізувати відміну, тощо.

# Приклад з життя:
# Пульт від телевізора: кожна кнопка — команда (ввімкнути, перемкнути канал).

# Простими словами:
# Навіщо: Щоб відокремити запит від його виконання.
# Як працює: Кожна команда — це окремий об’єкт з методом виконання.

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class TV:
    def on(self):
        print("TV is on")

    def off(self):
        print("TV is off")

class TVOnCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.on()

class TVOffCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self):
        self.tv.off()

class RemoteControl:
    def __init__(self):
        self.commands = {}

    def add_command(self, num_btn, command: Command):
        self.commands[num_btn] = command

    def press_btn(self, num_btn):
        return self.commands.get(num_btn).execute()

tv = TV()
remote = RemoteControl()

remote.add_command(1, TVOnCommand(tv))
remote.add_command(2, TVOffCommand(tv))
remote.press_btn(1)
remote.press_btn(2)

# -----------------

class Command:
    def execute(self):
        pass

class BackupCommand(Command):
    def execute(self):
        print("[CMD] Виконується резервне копіювання")

class EmailReportCommand(Command):
    def execute(self):
        print("[CMD] Відправлення звіту")

class CommandQueue:
    def __init__(self):
        self.queue = []

    def add_command(self, cmd):
        self.queue.append(cmd)

    def run(self):
        for cmd in self.queue:
            cmd.execute()

queue = CommandQueue()
queue.add_command(BackupCommand())
queue.add_command(EmailReportCommand())
queue.run()

# 8. State (Стан)
# Що це таке?
# Дозволяє об’єкту змінювати свою поведінку залежно від внутрішнього стану.

# Приклад з життя:
# Світлофор: у кожному стані (червоний, жовтий, зелений) його поведінка інша.

# Простими словами:
# Навіщо: Щоб уникати складних if-else при зміні стану.
# Як працює: Поведінка розбита на класи-состояния. Об’єкт делегує поведінку поточному стану.
class TrafficLightState(ABC):
    @abstractmethod
    def handle(self, traffic_light):
        pass

class RedState(TrafficLightState):
    def handle(self, traffic_light):
        print("Светофор: Червоний – СТОЙ!")
        traffic_light.state = GreenState()

class GreenState(TrafficLightState):
    def handle(self, traffic_light):
        print("Светофор: Зелений – Їдь!")
        traffic_light.state = YellowState()

class YellowState(TrafficLightState):
    def handle(self, traffic_light):
        print("Светофор: Жовтий – Готуйся!")
        traffic_light.state = RedState()

class TrafficLight:
    def __init__(self):
        self.state: TrafficLightState = RedState()

    def change(self):
        self.state.handle(self)

light = TrafficLight()
for _ in range(6):
    light.change()

# -----------------

class AccountState:
    def do_action(self):
        pass

class ActiveState(AccountState):
    def do_action(self):
        print("Користувач активний")

class BlockedState(AccountState):
    def do_action(self):
        print("Акаунт заблокований")

class Account:
    def __init__(self):
        self.state = ActiveState()

    def set_state(self, state):
        self.state = state

    def action(self):
        self.state.do_action()

acc = Account()
acc.action()
acc.set_state(BlockedState())
acc.action()

# 9. MVC (Модель-Вид-Контролер)
# Що це таке?
# Ділить програму на три компоненти:
# - Модель (Model): логіка, зберігання даних.
# - Вид (View): інтерфейс, відображення.
# - Контролер (Controller): приймає команди, керує логікою.

# Приклад з життя:
# Ресторан: кухня (модель), зал (вид), офіціант (контролер).

# Простими словами:
# Навіщо: Щоб спростити розділення відповідальностей.
# Як працює: Кожен компонент має свою чітку роль.

class Kitchen:
    def __init__(self):
        self.orders = {}

    def add_order(self, table, order):
        self.orders[table] = order
        print(f"Кухня: Прийнято замовлення від столика {table} – {order}")

    def get_order(self, table):
        return self.orders.get(table, "Замовлення не знайдено.")

class DiningRoom:
    def display_order(self, table, order):
        print(f"Зал: Столик {table} отримує замовлення: {order}")

class Waiter:
    def __init__(self, kitchen: Kitchen, dining_room: DiningRoom):
        self.kitchen = kitchen
        self.dining_room = dining_room

    def take_order(self, table, order):
        print(f"Офіціант: Прийняв замовлення від столика {table}.")
        self.kitchen.add_order(table, order)

    def serve_order(self, table):
        order = self.kitchen.get_order(table)
        self.dining_room.display_order(table, order)

# Тестування:
kitchen = Kitchen()
dining_room = DiningRoom()
waiter = Waiter(kitchen, dining_room)

waiter.take_order(5, "Піца Маргарита")
waiter.serve_order(5)

# -----------------

class User:
    def __init__(self, username):
        self.username = username

# Контролер
class UserController:
    def create_user(self, username):
        user = User(username)
        return UserView.render(user)

# Вид
class UserView:
    @staticmethod
    def render(user):
        return {"username": user.username, "status": "created"}

ctrl = UserController()
print(ctrl.create_user("andriy"))

# 10. Composite (Компонувальник)
# Що це таке?
# Дозволяє однаково працювати з окремими об’єктами і їх групами.

# Приклад з життя:
# Папка на комп’ютері — містить файли або інші папки. Копіювати можна і те, і те.
class FileSystemComponent(ABC):
    @abstractmethod
    def show_info(self, indent=0):
        pass

class File(FileSystemComponent):
    def __init__(self, name):
        self.name = name

    def show_info(self, indent=0):
        print(" " * indent + f"Файл: {self.name}")

class Folder(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def remove(self, component: FileSystemComponent):
        self.children.remove(component)

    def show_info(self, indent=0):
        print(" " * indent + f"Папка: {self.name}")
        for child in self.children:
            child.show_info(indent + 2)

root = Folder("Коренева")
doc_folder = Folder("Документи")
pic_folder = Folder("Фото")
file1 = File("резюме.docx")
file2 = File("відпустка.jpg")

doc_folder.add(file1)
pic_folder.add(file2)
root.add(doc_folder)
root.add(pic_folder)

root.show_info()

# -----------------

class FileSystemItem:
    def display(self, indent=0):
        pass

class File(FileSystemItem):
    def __init__(self, name):
        self.name = name

    def display(self, indent=0):
        print(" " * indent + f"Файл: {self.name}")

class Folder(FileSystemItem):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, item):
        self.children.append(item)

    def display(self, indent=0):
        print(" " * indent + f"Папка: {self.name}")
        for child in self.children:
            child.display(indent + 2)

root = Folder("root")
root.add(File("README.md"))
sub = Folder("src")
sub.add(File("main.py"))
root.add(sub)
root.display()