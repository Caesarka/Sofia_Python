from flask_restx import Namespace, Resource, reqparse, fields
import crud

api = Namespace('Tasks', description='one object task')

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


@api.route('/')
class Tasks(Resource):
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        id_filter = args.get('id')
        ids_filter = args.get('ids')
        title_filter = args.get('title')
        desc_filter = args.get('description')
        has_desc_filter = args.get('has_description')
        count = args.get('count')

        tasks = crud.readBD()
        context = tasks

        if id_filter:
            context = list(filter(lambda task: task['id'] == id_filter, tasks))

        if title_filter:
            context = list(filter(lambda task: title_filter.lower()
                           in task['title'].lower(), context))

        if desc_filter:
            context = list(filter(lambda task: desc_filter.lower()
                           in task['description'].lower(), context))

        if has_desc_filter == True:
            context = list(task for task in context if task.get(
                'description') and task['description'].strip())

        if has_desc_filter == False:
            context = list(task for task in context if not task.get(
                'description') or not task['description'].strip())

        if ids_filter:
            id_list = ids_filter.split(',')
            context = list(task for task in context if task['id'] in id_list)

        if count:
            context = context[:count]

        return context