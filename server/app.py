#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants_dict=[p.to_dict() for p in Plant.query.all()]

        r=make_response(plants_dict, 200)
        return r
    
    def post(self):
        json_input=request.get_json()
        new_plant=Plant(
            name=json_input['name'],
            image=json_input['image'],
            price=json_input['price'],
        )
        db.session.add(new_plant)
        db.session.commit()
        np_dict=new_plant.to_dict()
        r=make_response(np_dict, 201)
        return r



class PlantByID(Resource):
    def get(self, id):
        plant_dict=Plant.query.filter_by(id=id).first().to_dict()
        r=make_response(plant_dict, 200)
        return r
        

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
