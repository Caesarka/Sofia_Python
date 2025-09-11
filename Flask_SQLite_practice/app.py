from flask import Flask
from flask_restx import Api
import db
from api import ns as realty_ns

app = Flask(__name__)
api = Api(app, title="Realty API", doc="/")
api.add_namespace(realty_ns)

#close db after request
app.teardown_appcontext(db.close_db)

if __name__ == "__main__":
    db.init_db_if_needed()
    app.run(debug=True)


