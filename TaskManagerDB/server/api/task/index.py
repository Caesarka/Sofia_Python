from flask_restx import Namespace, Resource, reqparse, fields
import crud

api = Namespace('Task', description='one object task')

parser = reqparse.RequestParser()
parser.add_argument('id', type=str, required=False, help='id')
parser.add_argument('ids', type=str, required=False, help='set of id')
parser.add_argument('title', type=str, required=False, help='title')
parser.add_argument('description', type=str,
                    required=False, help='description')
parser.add_argument('has_description', type=lambda x: x.lower()
                    == 'true', required=False, help='flag description')
parser.add_argument('count', type=int, required=False, help='count on page')

hello_post = api.model('Hello', {
    'username': fields.String(required=True)
})

task_post = api.model('TaskPost', {
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(required=True, description='Task description')
})

task_update = api.model('TaskUpdate', {
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(required=True, description='Task description'),
    'status': fields.String(required=False),
    'priority': fields.String(required=False)
})

task_delete = api.model('TaskDelete', {
    'id': fields.String(required=True, description='Task ID'),
})

@api.route('/')
class Task(Resource):
    @api.expect(task_post, validate=True)
    @api.doc(description='Add new task into database')
    def put(self):
        data = api.payload
        title = data['title']
        description = data['description']

        try:
            new_task = crud.task_create(title, description)
            return {
                'id': new_task[0],
                'title': new_task[1],
                'description': new_task[2],
                'status': new_task[3],
                'priority': new_task[4]
            }, 201
        except Exception as e:
            return {'message': str(e)}, 404

@api.route('/<string:id>')
class Task(Resource):
    @api.doc(description='Get task')
    def get(self, id):
        try:
            task = crud.task_read(id)
            if task:
                return {
                    'id': task[0],
                    'title': task[1],
                    'description': task[2],
                    'status': task[3],
                    'priority': task[4]
                }, 200
            else:
                return {'message': f'Task {id} not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
    
    @api.expect(task_update, validate=True)
    @api.doc(description='Update existing task')
    def post(self, id):
        data = api.payload
        print(id, data)

        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        priority = data.get('priority')

        # try:
        task = crud.task_update(id, title, description, status, priority)
        return {
            'id': task[0],
            'title': task[1],
            'description': task[2],
            'status': task[3],
            'priority': task[4]
        }, 200
        # except Exception as e:
        #     return {'message': str(e)}, 404

    @api.doc(description='Delete task by ID')
    def delete(self, id):
        try:
            deleted = crud.task_delete(id)
            if deleted:
                return {'message': f'Task. {id} deleted'}, 200
            else:
                return {'message': f'Task {id} not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500


