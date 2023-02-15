from flask import Flask, request

# database setup through ORM: object-relational marker
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure database so we can connect to it.. sqlite databse called data.db in same directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


# classes for database connection:
class Drink(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(120))

    #overwrite another method, called the repr: we want to pass in "self" & get the object's attributes
    def __repr__(self):
        return f"{self.name} - {self.description}"


# routes for app:
@app.route('/')
def index():
    return 'Hello!'

# Getting all drinks
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []

    for drink in drinks:
        drink_data = {'name':drink.name, 'description': drink.description}

        output.append(drink_data)

    return {"drinks":output}

#  Getting a single drink via IDs - place/position in database
@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "drscription":drink.description}


# Adding a new drink:
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'],
                  description=request.json['description']
                )
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

    #use Postman to test parsing requests.. 

# Deleting a drink:
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)

    # if drink doesn't exist edge case:
    if drink is None:
        return {'error':"not found"}

    db.session.delete(drink)
    db.session.commit()
    return {"message":"drink deleted!"}