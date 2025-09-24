from flask import Flask, render_template, send_from_directory
from flask_restx import Api
from database import realty
from resources.realty import ns as realty_ns



app = Flask(__name__, template_folder='views', static_folder='static')

@app.get('/')
def index():
    # static rendering
    return render_template('index.html', cards=[
        {
            'id': 1,
            'price': 969000,
            'title': 'Condo Apartment',
            'city': 'Toronto',
            'address': 'Unit 611 - 10 Delisle Avenue',
        },
        {
            'id': 2,
            'price': 1599999,
            'title': 'Detached',
            'city': 'Mississauga',
            'address': '550 Meadows Blvd',
        },
        {
            'id': 3,
            'price': 719000,
            'title': 'Condo Townhouse',
            'city': 'Richmond Hill',
            'address': '1521 19th Ave',
        },
        {
            'id': 5,
            'price': 1390000,
            'title': 'Detached Bungalow',
            'city': 'Etobicoke',
            'address': '37 Sunplains Crescent',
        },
        {
            'id': 6,
            'price': 1949000,
            'title': 'Detached',
            'city': 'North York',
            'address': '14 Northmount Avenue',
        },
        {
            'id': 7,
            'price': 1399888,
            'title': 'Freehold Townhouse',
            'city': 'North York',
            'address': '299 Finch Avenue E',
        },
        {
            'id': 8,
            'price': 799000,
            'title': '3 bedroom apartment',
            'city': 'Toronto',
            'address': 'Unit 3307 - 82 Dalhousie Street',
        },
        {
            'id': 10,
            'price': 1890000,
            'title': 'Detached',
            'city': 'Toronto',
            'address': '61 Castle Knock Road',
        },
        {
            'id': 11,
            'price': 1449000,
            'title': 'Condo Apartment',
            'city': 'Toronto',
            'address': 'Unit 911 - 90 Stadium Road S',
        },
    ])


api = Api(app, title="Realty API", doc="/doc/")
api.add_namespace(realty_ns, path='/api/realty')


if __name__ == "__main__":
    realty.init_db_if_needed()
    app.run(debug=True)


