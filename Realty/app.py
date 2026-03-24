from flask import Flask, redirect, render_template, g, request, send_from_directory, session
from flask import make_response
from flask_restx import Api

from L2_Api_Controllers.auth.jwt_utils import jwt_required
from L2_Api_Controllers.realty_api_model import ns_realty
from L2_Api_Controllers.schemas.realty_model import RealtyPatch
from L2_Api_Controllers.user_api_model import ns_user
from L2_Api_Controllers import user_controller, realty_controller

from L3_Business_Logic.user_service import UserService

from L4_Data_Access.sql.session import init_db_if_needed_v1
from L4_Data_Access.orm.session import session_factory, init_db_if_needed_v2, get_session
#from api.user import Register, UserList, Login
init_db_if_needed_v1()
init_db_if_needed_v2()

app = Flask(__name__, template_folder='L1_Html_Client/views', static_folder='L1_Html_Client/assets', static_url_path='/assets')
app.secret_key = "supersecret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssr')
@jwt_required(optional=True)
def ssr():
    return redirect('/ssr/realties')

@app.route('/ssr/realties')
@jwt_required(optional=True)
def ssr_realties():
    realties = realty_controller.RealtyService(get_session()).get_all_active_realties()
    return render_template('pages/realties.html', realties=realties)

@app.route('/ssr/login')
@jwt_required(optional=True)
def ssr_login():
    return render_template('pages/login.html', user=request.user)

@app.route('/ssr/register')
@jwt_required(optional=True)
def ssr_register():
    return render_template('pages/register.html')

@app.route('/ssr/about')
@jwt_required(optional=True)
def ssr_about():
    return render_template('pages/about.html')

@app.route('/ssr/profile')
@jwt_required()
def ssr_profile():
    if not request.user:
        return redirect('ssr/login')
    
    DBSession = get_session()
    try:
        user_id = request.user["user_id"]
        user = UserService(DBSession).get_user_by_id(user_id)
        realties = []
        favorites = []

        if request.user.get("role") in ["realtor", "admin"]:
            realties = realty_controller.RealtyService(DBSession).get_my_realties(
                user_id,
                is_deleted=False,
            )
        elif request.user.get("role") == "buyer":
            favorites = realty_controller.RealtyService(DBSession).get_saved_realties(
                user_id,
                status="active",
            )

        return render_template('pages/profile.html', user=user, realties=realties, favorites=favorites)
    finally:
        DBSession.close()

@app.route('/ssr/logout', methods=['POST'])
@jwt_required(optional=True)
def ssr_logout():
    response = make_response(redirect('/ssr'))
    response.set_cookie("access_token", "", expires=0, httponly=True, samesite="Strict")
    return response

@app.route('/ssr/realty/create', methods=['GET', 'POST'])
@jwt_required()
def ssr_create_realty_page():
    if request.user.get("role") not in ["realtor", "admin"]:
        return redirect('/ssr/profile')

    if request.method == 'GET':
        return render_template('pages/create_realty.html')

    DBSession = get_session()
    try:
        realty_data = {
            "title": request.form.get("title"),
            "price": request.form.get("price"),
            "city": request.form.get("city"),
            "address": request.form.get("address"),
            "image": request.form.get("image") or "/assets/default.jpg",
            "user_id": request.user["user_id"],
        }
        realty_controller.RealtyService(DBSession).create_realty(realty_data)
        return redirect('/ssr/profile')
    finally:
        DBSession.close()

@app.route('/ssr/realty/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required()
def ssr_patch_realty(id):
    if request.user.get("role") not in ["realtor", "admin"]:
        return redirect('/ssr/profile')
    
    DBSession = get_session()
    try:
        realty_service = realty_controller.RealtyService(DBSession)
        realty = realty_service.get_realty(id)

        if request.user.get("role") == "realtor" and realty.user_id != request.user["user_id"]:
            return redirect('/ssr/profile')
        
        if request.method == 'GET':
            return render_template('pages/edit_realty.html', realty=realty)
        
        patch_data = RealtyPatch(
            title=request.form.get("title"),
            price=request.form.get("price"),
            city=request.form.get("city"),
            address=request.form.get("address"),
            image=request.form.get("image") or "/assets/default.jpg",
        )
        realty_service.patch_realty(patch_data, id)
        return redirect('/ssr/profile')
    finally:
        DBSession.close()


@app.route('/ssr/realty/<int:id>/delete', methods=['POST', 'DELETE'])
@jwt_required()
def ssr_delete_realty(id):
    if request.user.get("role") not in ["realtor", "admin"]:
        return redirect('/ssr/profile')
    
    DBSession = get_session()
    try:
        realty_service = realty_controller.RealtyService(DBSession)
        realty = realty_service.get_realty(id)

        if request.user.get("role") == "realtor" and realty.user_id != request.user["user_id"]:
            return redirect('/ssr/profile')
        
        realty_service.delete_realty(id)
        return redirect('/ssr/profile')
    finally:
        DBSession.close()

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
