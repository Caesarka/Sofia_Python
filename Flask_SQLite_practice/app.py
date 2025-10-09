from flask import Flask, render_template
from flask_restx import Api
from db import init_db_if_needed
#from services.realty import sql as realty_sql
#from services.user import sql as user_sql
from api_models.realty_api_model import ns_realty
from api_models.user_api_model import ns_user
from controllers import user_controller, realty_controller


init_db_if_needed()

app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = "supersecret"
api = Api(app, title="My API", doc="/doc/")

api.add_namespace(ns_realty, path='/api/realty')
api.add_namespace(ns_user, path='/api/user')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
