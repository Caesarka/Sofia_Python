from flask import Flask, render_template, g, send_from_directory
from flask_restx import Api
from L2_Api_Controllers.auth.jwt_utils import jwt_required
from L4_Data_Access.sql.session import init_db_if_needed_v1
from L2_Api_Controllers.realty_api_model import ns_realty
from L2_Api_Controllers.user_api_model import ns_user
from L2_Api_Controllers import user_controller, realty_controller
from L4_Data_Access.orm.session import session_factory, init_db_if_needed_v2, get_session
#from api.user import Register, UserList, Login
init_db_if_needed_v1()
init_db_if_needed_v2()

app = Flask(__name__, template_folder='L1_Html_Client/views', static_folder='L1_Html_Client/assets', static_url_path='/assets')
app.secret_key = "supersecret"

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/login', methods=['POST'])
#def testPostLogin():
#    return 'hahaha'

@app.route('/ssr')
def ssr():
    realties = realty_controller.RealtyService(get_session()).get_all_active_realties()
    return render_template('ssr.html', realties=realties)


@app.route('/ssr/login')
@jwt_required(optional=True)
def ssr_login():
    return render_template('pages/login.html')

@app.route('/ssr/register')
@jwt_required(optional=True)
def ssr_register():
    return render_template('pages/register.html')

@app.route('/ssr/about')
@jwt_required(optional=True)
def ssr_about():
    return render_template('pages/about.html')

@app.route('/ssr/profile')
@jwt_required(optional=True)
def ssr_profile():
    return render_template('pages/profile.html')

api = Api(app, title="My API", doc="/doc/")
api.add_namespace(ns_realty, path='/api/realty')
api.add_namespace(ns_user, path='/api/user')


#@app.before_request
#def create_session_db():
#    get_session()
    
#@app.teardown_request
#def teardown_db(exception=None):
#    close_db_session(exception)

# The fallback route
@app.route("/csr", defaults={"path": ""})
@app.route("/csr/<path:path>")
def csrFallback(path):
    # Log the path or handle it as needed
    print(f"Fallback route triggered for path: {path}")
    # For a SPA, you might return the index.html file
    return send_from_directory(app.static_folder, "csr.html")

@app.route("/vue", defaults={"path": ""})
@app.route("/vue/<path:path>")
def vue_fallback(path):
    return send_from_directory(app.static_folder, "vue.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
