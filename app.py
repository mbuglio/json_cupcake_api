from flask import Flask, request,jsonify,render_template
from models import Cupcake, connect_db, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:K1ashmir!@localhost:5432/cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '12234joijwef'

connect_db(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        rating = data['rating'],
        size = data['size'],
        image = data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()

    return(jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api.cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor= data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')




