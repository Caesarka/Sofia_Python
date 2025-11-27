from flask import Flask, render_template, g
from flask_restx import Api
from db_sql import init_db_if_needed_v1
from api_models.realty_api_model import ns_realty
from api_models.user_api_model import ns_user
from controllers import user_controller, realty_controller
from db.session import session_factory, close_db_session, init_db_if_needed_v2, get_session
#from api.user import Register, UserList, Login
init_db_if_needed_v1()
init_db_if_needed_v2()

app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = "supersecret"




api = Api(app, title="My API", doc="/doc/")

api.add_namespace(ns_realty, path='/api/realty')
api.add_namespace(ns_user, path='/api/user')

#@app.before_request
#def create_session_db():
#    get_session()
    
#@app.teardown_request
#def teardown_db(exception=None):
#    close_db_session(exception)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
