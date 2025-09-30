from flask import Flask, render_template, send_from_directory
from flask_restx import Api
from database import realty
from services.realty import sql as realty_sql
from services.user import sql as user_sql
from resources.realty import ns_realty
from resources.user import ns_user



app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = "supersecret"

api = Api(app, title="My API", doc="/doc/")

api.add_namespace(ns_realty, path='/api/realty')
api.add_namespace(ns_user, path='/api/user')

#@app.teardown_appcontext
#def close_realty_db(error):
    #realty.close_db()

@app.route("/realty")
def realty_page():
    filter_data = {"city": None, "min_price": None, "max_price": None}
    rows = realty_sql.get_by_filter(filter_data)
    return render_template("realty_switch.html", cards=rows)

@app.route("/user/<int:user_id>")
def user_page(user_id):
    row = user_sql.execute_data("get_user", {'id': user_id})
    if not row:
        return {"message": "User not found"}, 404
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "status": row["status"]
    }

if __name__ == "__main__":
    realty.init_db_if_needed()
    app.run(host="0.0.0.0", port=8080, debug=True)
