import sqlite3
from flask import Flask, g
from pathlib import Path
from flask_restx import Api, Resource, fields
#from controllers.controller import RealtyAll

path = Path("realty.db")

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def row_to_dict(row: sqlite3.Row):
    return dict(row) if row is not None else None

app = Flask(__name__)
api = Api(app)
ns = api.namespace("realty", description="Real Estate")

realty_model = api.model('Realty', {
    'id': fields.Integer(required=True, description='ID'),
    'title': fields.String(required=True, description='Name'),
    'price': fields.Integer(required=True, description='Price'),
    'city': fields.String(required=True, description='City')
})

    
# Регистрация маршрута
#@app.route("/api/v1/realty/{id}", methods=['GET', 'PUT', 'DELETE'])
#def home():
#    if request.method == 'DELETE':
#        return 'запись удалена...'
#    return "Hello"
#
#@app.get('/g')
#def g():
#    pass
#
#@app.post('/h')
#def h():
#    pass
#

@api.route("/api/v1/realty")
class RealtyAll(Resource):
    @api.doc(description="Get all realties")
    @api.marshal_list_with(realty_model)
    def get(self):
        rows = get_db().execute("SELECT * FROM realty").fetchall()
        return [row_to_dict(r) for r in rows]
    

        #realties = session.query(RealtyModel).all()
        #return [{"id": realty.id, "title": realty.title, "price": realty.price, "city": realty.city}for realty in realties]
    
#    @api.doc(description="Add new realty")
#    @api.expect(realty_model)
#    @api.marshal_with(realty_model)
#    def post(self):
#        data = api.payload
#        new_realty = RealtyModel(data)
#        session.add(new_realty)
#        session.commit()
#        return data, 201



if __name__ == "__main__":
    with app.app_context():
        get_db().executescript(Path("schema.sql").read_text())
        get_db().commit()
    app.run(debug=True)