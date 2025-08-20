import crud
import requests
import threading
import time
from flask import Flask, render_template, request, jsonify
from flask_restx import Resource, Api, reqparse, fields
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from api.task.index import api as api_task
from api.tasks.index import api as api_tasks
from server.model.user.user_models import *
from server.model.user.user_manager import UserManager

app = Flask(__name__, template_folder='views')
app.secret_key = "wlfnkwgnbkjerngjerbgi"

api = Api(app)
login_manager = LoginManager(app)

api.add_namespace(api_tasks, path='/tasks')
api.add_namespace(api_task, path='/task')

test_username = 'user_name'
test_pwd = 'password'

#engine = create_engine("sqlite:///to_do_data.db", echo=True)

#user_manager = UserManager(engine)



# 1. Описать роут /login по методу POST который принимает username и password
# 2. Описать произвольный роут /user по методу GET (будет отдавать информацию о пользователе, если тот авторизован)
# 3. Описать метод POST роут /logout


class User(UserMixin):
    def __init__(self, user_id, user_name, first_name='', last_name=''):
        super().__init__()
        self.id = str(user_id)
        self.name = user_name
        self.first_name = first_name
        self.last_name = last_name

test_user = User(1, test_username, first_name='Julianna', last_name='Gusarova')

@login_manager.user_loader
def load_user(uid: str):
    return test_user if uid == test_user.id else None

user_login = api.model('User Login', {
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
})

user_info = api.model('User info', {
    'first_name': fields.String(required=True, description='first name'),
    'last_name': fields.String(required=True, description='last name'),
})

@api.route('/login')
class Login(Resource):
    @api.expect(user_login, validate=True)
    @api.doc(description='User Login')
    def post(self):
        data = api.payload
        result = user_manager.check_user_password(data['username'], data['password'])
        
        if result:
            login_user(test_user, remember=True)
            return {'message': 'ok'}, 200
        return {'error': 'wrong data'}, 401


@api.route('/user')
class UserResource(Resource):
    @api.doc(description='Get user info')
    @api.marshal_with(user_info)
    @login_required
    def get(self):
        return {
            'first_name': test_user.first_name,
            'last_name': test_user.last_name
            }


@api.route('/logout')
class Logout(Resource):
    @api.doc(description='Logout current user')
    @login_required
    def post(self):
        logout_user()
        return {'message': 'logged out'}, 200
    
# def get_data(id):
#    # res = requests.get(f'http://127.0.0.1:5000/tasks?id={id}')
#    params = { 'id': id}
#    res = requests.get(f'http://127.0.0.1:5000/tasks', params=params)
#    print(res.json)
#    print(res.url)
#    print(res.status_code)
#    time.sleep(1)
#    print(res.headers)
#    print('------------')
#
# th1 = threading.Thread(target=get_data, args=(1, ))
# th2 = threading.Thread(target=get_data, args=(2, ))
#
# th1.start()
# th2.start()
#
# api_urls = {
#    'GET_ALL_TASKS': '/tasks',
#    'GET_ALL_TASK': '/tasks'
# }
#
# BASE_URL = 'http://127.0.0.1:5000'
# def GET(url_method, params={}):
#    res = requests.get(f'{BASE_URL}{api_urls[url_method]}', params=params)
#

# 1. Создать папку api, в ней разместить файл api.py
# 2. В файле описать отедльными функциями запросы на получение, удаление, изменение и отправку данных
# Каждая функция должна возвращать готовый для использования объект
# 3. В папке utils описать класс DataWorket, который наследует класс threading.Thread и определяет методы, которые будут вызывать события на тот или иной метод запросов и обновляет данные. Логика следующая:
# – В приложении нужно будет добавить кнопку обновления. Кнопка обновления вызывает метод треда,
# который в свою очередь выполняет запрос. Также кнопка передает в метод треда функцию, которая должна выполниться ПОСЛЕ завершения запроса.
# – Сделать такие же методы для отправки других видов запросов


'''
tasks = [
    {
        'id': '1',
        'title': 'SINs',
        'description': 'Find Ontario Service near by. Check they accept TR'
    },
    {
        'id': '2',
        'title': 'Find a home',
        'description': 'View listings. Find an agent and go to shoings'
    },
    {
        'id': '3',
        'title': 'Bathroom rugs',
        'description': 'Home Depot, Canadian tire?'
    },
    {
        'id': '4',
        'title': 'Apply for OHIP',
        'description': None
    },
    {
        'id': '5',
        'title': 'certified translation of driver\'s license',
        'description': 'find a licensed translator'
    },
    {
        'id': '6',
        'title': 'Ask hydro for delivery price',
        'description': None
    },
    {
        'id': '7',
        'title': 'Refund on a stroller',
        'description': 'send a refund request to the airline + photo of the stroller'
    },
    {
        'id': '8',
        'title': 'Find baby formulas with goat milk',
        'description': 'Metro, Freshco, Loblaws? Ask in chat'
    },
    {
        'id': '9',
        'title': 'Ask the company to hold the container until December 15th',
        'description': 'info@containercorp.com, +1 905-764-3777'
    },
    {
        'id': '10',
        'title': 'Find a pediatrician',
        'description': 'after we find rent!'
    }
]
'''

# tasks = crud.readBD()


if __name__ == '__main__':
    app.run(debug=True)
