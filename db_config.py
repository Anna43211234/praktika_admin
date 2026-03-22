import mysql.connector
from mysql.connector import Error
from datetime import datetime


class DBConnection:
    # Инициализация параметров подключения к базе данных
    def __init__(self):
        self.host = 'MySQL-8.4'
        self.user = 'root'
        self.password = ''
        self.database = 'admin_panel'  # Изменено на вашу БД
        self.connection = None
        self.cursor = None

    # Установка соединения с базой данных
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                use_unicode=True
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print("База данных подключена")
            return True
        # Обработка ошибки подключения
        except Error as e:
            print(f"Ошибка подключения: {e}")
            return False

    # Закрытие соединения с базой данных
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Соединение с БД закрыто")

    # Проверка учетных данных пользователя
    def check_user(self, username, password):
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()

            # Если пользователь найден, обновляем время последнего входа
            if user:
                self.update_last_login(user['id'])

            return user
        except Error as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return None

    # Обновление времени последнего входа
    def update_last_login(self, user_id):
        try:
            query = "UPDATE users SET last_login = NOW() WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
        except Error as e:
            print(f"Ошибка при обновлении last_login: {e}")

    # Получение всех пользователей
    def get_all_users(self):
        try:
            self.cursor.execute("SELECT id, username, email, full_name, last_login, created_at FROM users")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении списка пользователей: {e}")
            return []

    # Добавление записи в лог действий
    def add_log(self, username, action):
        try:
            query = "INSERT INTO admin_logs (username, action) VALUES (%s, %s)"
            self.cursor.execute(query, (username, action))
            self.connection.commit()
        except Error as e:
            print(f"Ошибка при добавлении лога: {e}")

    # Получение логов действий
    def get_logs(self, limit=50):
        try:
            query = "SELECT * FROM admin_logs ORDER BY action_time DESC LIMIT %s"
            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении логов: {e}")
            return []