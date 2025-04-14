# Імпортуємо необхідні модулі з Flask
from flask import Flask, jsonify

# Ініціалізуємо Flask-додаток
app = Flask(__name__)

# Простий "псевдо"-словник користувачів (імітація бази даних)
users_db = {
    "user1" : {"name": "Alice", "role": "admin"},
    "user2" : {"name": "Bob", "role": "user"},
}

# Роут для отримання інформації про користувача за ім’ям
@app.route("/api/users/<username>", methods = ["GET"])
def get_user(username):
    # Отримуємо користувача зі словника
    user = users_db.get(username)

    # Якщо користувач знайдений — повертаємо його дані
    if user:
        return jsonify({"username": username, "data": user}), 200
    # Якщо не знайдений — повідомляємо про помилку
    return jsonify({"error": "User not found"}), 404

# Запускаємо додаток тільки якщо файл виконується напряму
if __name__ == "__main__":
    app.run(debug=True)
