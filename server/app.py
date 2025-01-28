#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    """Create a new baked good."""
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=float(data.get('price')),  # Ensure price is stored as a float
        bakery_id=int(data.get('bakery_id'))  # Convert bakery_id to int
    )
    db.session.add(new_baked_good)
    db.session.commit()
    return make_response(new_baked_good.to_dict(), 201)

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    """Update the name of a bakery."""
    data = request.form
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)
    
    bakery.name = data.get('name', bakery.name)  # Update name if provided
    db.session.commit()
    return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    """Delete a baked good by ID."""
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return make_response({"error": "Baked good not found"}, 404)
    
    db.session.delete(baked_good)
    db.session.commit()
    return make_response({"message": "Baked good deleted successfully"}, 200)
