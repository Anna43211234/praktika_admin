from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from db_config import DBConnection
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Измените на свой секретный ключ

# Данные администрации (взяты с сайта-справочника)
admin_data = {
    'title': 'Администрация Глазовского района',
    'address': 'ул. Молодой Гвардии, 22а, г. Глазов, Удмуртская Республика, 427620',
    'phone_main': '+7 (34141) 2-25-75',
    'phone_fax': '+7 (34141) 2-25-58',
    'email': 'admin@glazov-raion.ru',
    'work_hours': 'Пн-Пт: 8:00 – 17:00 (обед: 12:00 – 13:00)',
    'head': 'Глава муниципального образования "Глазовский район"',
    'departments': [
        {'name': 'Приемная', 'phone': '+7 (34141) 2-25-75'},
        {'name': 'Глава района', 'phone': '+7 (34141) 2-25-58'},
        {'name': 'Председатель Совета Депутатов', 'phone': '+7 (34141) 5-69-59'},
        {'name': 'Зам. главы по экономике и финансам', 'phone': '+7 (34141) 2-95-93'},
        {'name': 'Управление сельского хозяйства', 'phone': '+7 (34141) 5-27-67'},
        {'name': 'Зам. главы по социальным вопросам', 'phone': '+7 (34141) 7-20-05'},
        {'name': 'Зам. главы по строительству и ЖКХ', 'phone': '+7 (34141) 7-20-52'},
        {'name': 'Правовой отдел', 'phone': '+7 (34141) 5-27-69'},
        {'name': 'Бухгалтерия', 'phone': '+7 (34141) 5-29-98'},
        {'name': 'Отдел имущественных отношений', 'phone': '+7 (34141) 5-41-36'},
        {'name': 'Отдел ЖКХ, транспорта и связи', 'phone': '+7 (34141) 7-12-47'},
        {'name': 'Отдел архитектуры и строительства', 'phone': '+7 (34141) 5-43-21'},
        {'name': 'Отдел по делам ГО и ЧС', 'phone': '+7 (34141) 2-98-51'},
        {'name': 'Отдел опеки и попечительства', 'phone': '+7 (34141) 7-23-34'},
        {'name': 'Управление образования', 'phone': '+7 (34141) 5-88-94'},
        {'name': 'Отдел общего и доп. образования', 'phone': '+7 (34141) 5-27-68'},
        {'name': 'Отдел физкультуры и спорта', 'phone': '+7 (34141) 3-15-50'},
        {'name': 'Отдел культуры и молодежной политики', 'phone': '+7 (34141) 5-33-18'},
        {'name': 'ЗАГС', 'phone': 'информация уточняется'},
    ]
}


# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return render_template('app.html', data=admin_data, logged_in='user_id' in session)


@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = DBConnection()
        if db.connect():
            user = db.check_user(username, password)

            if user:
                # Сохраняем данные пользователя в сессии
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user['full_name']
                session['email'] = user['email']

                # Логируем действие
                db.add_log(username, 'Вход в систему')
                db.disconnect()

                flash(f'Добро пожаловать, {user["full_name"]}!', 'success')
                return redirect(url_for('admin_panel'))
            else:
                db.disconnect()
                flash('Неверное имя пользователя или пароль', 'danger')
        else:
            flash('Ошибка подключения к базе данных', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Логируем выход
    if 'username' in session:
        db = DBConnection()
        if db.connect():
            db.add_log(session['username'], 'Выход из системы')
            db.disconnect()

    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))


@app.route('/admin-panel')
@login_required
def admin_panel():
    db = DBConnection()
    users = []
    logs = []

    if db.connect():
        users = db.get_all_users()
        logs = db.get_logs(20)  # Последние 20 действий
        db.disconnect()

    return render_template('admin_panel.html',
                           users=users,
                           logs=logs,
                           full_name=session.get('full_name'),
                           username=session.get('username'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                           user=session,
                           title='Профиль пользователя')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Здесь можно добавить логику сброса пароля
        flash('Инструкция по сбросу пароля отправлена на ваш email', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)