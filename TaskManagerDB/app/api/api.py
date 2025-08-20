import threading
import time
import requests


class ApiRequests():

    def __init__(self):
        self.BASE_URL = 'http://127.0.0.1:5000'
        self.api_urls = {
            'GET_TASKS': '/tasks',
            'GET_TASK': '/task',
            'DELETE_TASK': '/task',
            'POST_TASK': '/tasks',
            'PUT_TASK': '/task'
        }

    def validate(self, res):
        if res:
            return res.json()
        else:
            return res.text

    def GET(self, url_method, data={}, id=None):
        _id = f'/{id}' if id else ''

        res = requests.get(
            f'{self.BASE_URL}{self.api_urls[url_method]}{_id}', json=data)
        return self.validate(res)

    def DELETE(self, url_method, params={}, id=None):
        _id = f'/{id}' if id else ''
        res = requests.delete(
            f'{self.BASE_URL}{self.api_urls[url_method]}{_id}', params=params)
        return self.validate(res)

    def POST(self, url_method, data={}):
        res = requests.post(
            f'{self.BASE_URL}{self.api_urls[url_method]}', json=data)
        return self.validate(res)

    def PUT(self, url_method, data={}, id=None):
        _id = f'/{id}' if id else ''
        url = f'{self.BASE_URL}{self.api_urls[url_method]}{_id}'
        
        res = requests.put(url, json=data)
        return self.validate(res)

    def get_data(self, id):
        res = requests.get(f'http://127.0.0.1:5000/tasks?id={id}')
        print(res.json)
        print(res.url)
        print(res.status_code)
        time.sleep(1)
        print(res.headers)
        print('------------')

    def post_data(self):
        title = 'New Task Title'
        description = 'New Task Description'
        res = requests.post(f'http://127.0.0.1:5000/tasks?')
        print(res.json)
        print(res.url)
        print(res.status_code)
        time.sleep(1)
        print(res.headers)
        print('------------')

# th1 = threading.Thread(target=get_data, args=(1, ))
# th2 = threading.Thread(target=get_data, args=(2, ))
#
# th1.start()
# th2.start()


if __name__ == '__main__':
    api_requests = ApiRequests()
    print('GET_ALL')
    print(api_requests.GET('GET_TASKS'))
    print('GET_TASK_WO_ID')
    print(api_requests.GET('GET_TASK'))
    print('GET_TASK_ID')
    print(api_requests.GET('GET_TASK', id=1))
    print('DELETE')
    print(api_requests.DELETE('DELETE_TASK', id=14))
    print('POST')
    print(api_requests.POST('POST_TASK', {
                'title': 'My title2',
                'description': 'My description2'
    
    }))
    print('PUT')
    print(api_requests.PUT('PUT_TASK', {
                'title': 'My title changed',
                'description': 'My description changed'
    }, id=12))

