from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, timedelta

# ---------- Підключення до бази даних та налаштування ----------
# Створюємо двигун для SQLite бази example.sqlite
engine = create_engine("sqlite:///example.sqlite")
# Підключаємось до бази
conn = engine.connect()
# Об'єкт для метаданих таблиць
metadata = db.MetaData()

# ---------- Визначення таблиці Student (рівень Core) ----------
Student = db.Table(
    "Student", metadata,
    db.Column("Id", db.Integer, primary_key=True),
    db.Column("Name", db.String(255), nullable=False),
    db.Column("Major", db.String(255), default="Math"),
    db.Column("Pass", db.Boolean, default=True)
)
# Створюємо таблицю, якщо її ще не існує
metadata.create_all(engine)

# ---------- Вставка записів у таблицю Student ----------
# Вставляємо одного студента через insert().values()
query = db.insert(Student).values(Id=1, Name="Bob", Major="English", Pass=True)
conn.execute(query)
conn.commit()

# Виводимо всі записи таблиці
output = conn.execute(Student.select()).fetchall()
print(output)

# Масова вставка декількох записів
query = db.insert(Student)
values_list = [
    {"Id": 2, "Name": "Alice", "Major": "Science", "Pass": False},
    {"Id": 3, "Name": "Ben", "Major": "Math", "Pass": True},
    {"Id": 4, "Name": "John", "Major": "English", "Pass": False}
]
conn.execute(query, values_list)
conn.commit()
print(conn.execute(Student.select()).fetchall())

# ---------- CRUD: READ, UPDATE, DELETE для Student ----------
# Фільтрація за Major == 'English'
query = Student.select().where(Student.columns.Major == "English")
print(conn.execute(query).fetchall())

# Оновлення: позначаємо Pass=True для Alice
query = Student.update().values(Pass=True).where(Student.columns.Name == "Alice")
conn.execute(query)
conn.commit()
print(conn.execute(Student.select()).fetchall())

# Видалення: видаляємо запис Ben
query = Student.delete().where(Student.columns.Name == "Ben")
conn.execute(query)
conn.commit()
print(conn.execute(Student.select()).fetchall())

# ---------- Визначення та заповнення таблиць Divisions і Matchs ----------
Divisions = db.Table(
    "Divisions", metadata,
    db.Column("Division", db.String(10), primary_key=True),
    db.Column("Name", db.String(255)),
    db.Column("Country", db.String(255))
)
Matchs = db.Table(
    "Matchs", metadata,
    db.Column("Id", db.Integer, primary_key=True),
    db.Column("Div", db.String(10)),
    db.Column("HomeTeam", db.String(255)),
    db.Column("FTHG", db.Integer),
    db.Column("FTAG", db.Integer)
)
# Створюємо нові таблиці
metadata.create_all(engine)

# Вставляємо дані в Divisions
conn.execute(db.insert(Divisions), [
    {'Division': "E1", "Name": "Premier League", "Country": "England"},
    {'Division': "D1", "Name": "Bundesliga", "Country": "Germany"}
])
# Вставляємо дані в Matchs
conn.execute(db.insert(Matchs), [
    {"Div": "E1", "HomeTeam": "Norwich", "FTHG": 1, "FTAG": 1},
    {"Div": "E1", "HomeTeam": "Liverpool", "FTHG": 2, "FTAG": 1},
    {"Div": "D1", "HomeTeam": "Bayern", "FTHG": 3, "FTAG": 0}
])
conn.commit()

# Приклад JOIN між Matchs та Divisions
query_join = db.join(Matchs, Divisions, Matchs.c.Div == Divisions.c.Division)
query_select = db.select(
    Divisions.c.Division,
    Divisions.c.Name,
    Divisions.c.Country,
    Matchs.c.HomeTeam,
    Matchs.c.FTHG,
    Matchs.c.FTAG
).select_from(query_join)
result = conn.execute(query_select).fetchall()
for row in result:
    print(row)

# ---------- ORM: приклад з користувачем User ----------
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # Унікальний ідентифікатор
    username = Column(String)              # Ім'я користувача
    email = Column(String)                 # Електронна пошта

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

# Використовуємо окремий файл БД для ORM прикладу
enorm = create_engine("sqlite:///example.db", echo=False)
Base.metadata.create_all(enorm)
Session = sessionmaker(bind=enorm)
session = Session()

# Додаємо нового користувача
new_user = User(username="JohnDoe", email="john@example.com")
session.add(new_user)
session.commit()
# Читаємо та оновлюємо користувача
user = session.query(User).filter_by(username="JohnDoe").first()
print(f"Знайдено користувача: {user}")
user.email = "john.doe@example.com"
session.commit()
user = session.query(User).filter_by(username="JohnDoe").first()
print(f"Оновлено користувача: {user}")
# Видаляємо користувача
session.delete(user)
session.commit()
user = session.query(User).filter_by(username="JohnDoe").first()
print(f"Після видалення: {user}")

# ---------- ORM: ресторанні столики та бронювання ----------
Base = declarative_base()

class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True)
    seats = Column(Integer, nullable=False)  # Кількість місць за столом
    reservations = relationship("Reservation", back_populates="table")

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    reserved_at = Column(DateTime, nullable=False)  # Час бронювання
    duration_minutes = Column(Integer, default=60) # Тривалість бронювання в хвилинах
    table = relationship("Table", back_populates="reservations")

engine = create_engine("sqlite:///restaurant.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Функція додавання столика
def add_table(seats):
    table = Table(seats=seats)
    session.add(table)
    session.commit()
    print(f"Додано столик на {seats} місць")

# Функція бронювання столика
def book_table(requested_seats, desired_time):
    tables = session.query(Table).filter(Table.seats >= requested_seats)
    for table in tables:
        # Перевіряємо наявні бронювання
        reservations = session.query(Reservation).filter_by(table_id=table.id).all()
        conflict = False
        for res in reservations:
            res_start = res.reserved_at
            res_end = res.reserved_at + timedelta(minutes=res.duration_minutes)
            desired_end = desired_time + timedelta(minutes=60)
            # Перевірка перекриття інтервалів
            if not (desired_end <= res_start or desired_time >= res_end):
                conflict = True
                break
        if not conflict:
            reservation = Reservation(table=table, reserved_at=desired_time, duration_minutes=60)
            session.add(reservation)
            session.commit()
            print(f"Заброньвано столик #{table.id} на {desired_time.strftime('%d.%m.%Y %H:%M')}")
            return
    print("Немає вільних столиків на цей час")

# Приклади викликів функцій бронювання\add_table(2)
add_table(4)
book_table(2, datetime(2025, 4, 17, 18, 0))
book_table(2, datetime(2025, 4, 17, 18, 0))
book_table(2, datetime(2025, 4, 17, 18, 0))
book_table(2, datetime(2025, 4, 17, 19, 0))
book_table(4, datetime(2025, 4, 17, 19, 0))

# ---------- ORM: школа — студенти, предмети, оцінки ----------
Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)   # Ім'я студента
    group = Column(String, nullable=False)  # Група студента
    grades = relationship("Grade", back_populates="student")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)   # Назва предмету
    grades = relationship("Grade", back_populates="subject")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    value = Column(db.Float, nullable=False)  # Оцінка студента
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

# Підключення до school.db та створення таблиць
engine = create_engine("sqlite:///school.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Функція додавання студента
def add_student(name, group):
    student = Student(name=name, group=group)
    session.add(student)
    session.commit()
    print(f"Додано студента {name} до групи {group}")

# Функція додавання предмету
def add_subject(name):
    subject = Subject(name=name)
    session.add(subject)
    session.commit()
    print(f"Додано предмет {name}")

# Функція виставлення оцінки

def give_grade(student_name, subject_name, value):
    student = session.query(Student).filter_by(name=student_name).first()
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if not student or not subject:
        print("Студент або предмет не знайдені")
        return
    grade = Grade(student=student, subject=subject, value=value)
    session.add(grade)
    session.commit()
    print(f"Виставлено оцінку {value} студенту {student_name} з предмету {subject_name}")

# Функція обчислення середнього бала студента

def student_average(name):
    student = session.query(Student).filter_by(name=name).first()
    if not student:
        print("Студента не знайдено")
        return
    grades = [g.value for g in student.grades]
    if grades:
        avg = sum(grades) / len(grades)
        print(f"Середній бал {name}: {avg:.2f}")
    else:
        print(f"Оцінки для {name} не знайдені")

# Функція обчислення середнього бала з предмету

def subject_average(name):
    subject = session.query(Subject).filter_by(name=name).first()
    if not subject:
        print("Предмет не знайдено")
        return
    grades = [g.value for g in subject.grades]
    if grades:
        avg = sum(grades) / len(grades)
        print(f"Середній бал з {name}: {avg:.2f}")
    else:
        print(f"Оцінки з {name} не знайдені")

# Функція виведення студентів з відзнакою

def list_honors():
    print("Студенти з відзнакою (>=90):")
    for student in session.query(Student).all():
        grades = [g.value for g in student.grades]
        if grades:
            avg = sum(grades) / len(grades)
            if avg >= 90:
                print(f"{student.name} (середній бал: {avg:.2f})")

# ---------- Приклади використання функцій ----------
add_student("Bob", "Python")
add_student("Alice", "Python")
add_student("John", "Python")

add_subject("Math")
add_subject("English")

give_grade("Bob", "Math", 95)
give_grade("Alice", "Math", 100)
give_grade("Alice", "English", 85)
give_grade("John", "English", 90)
give_grade("Bob", "English", 60)

student_average("Bob")
student_average("Alice")
student_average("John")

subject_average("Math")
subject_average("English")

list_honors()
