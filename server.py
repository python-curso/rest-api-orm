# -*- coding: utf-8 -*-
import os
import base64
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from json import dumps
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from modal import db, User, app, users_schema, user_schema
from flask_marshmallow import Marshmallow

UPLOAD_FOLDER = 'folder'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

CORS(app)
api = Api(app)

ma = Marshmallow(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Users(Resource):
    def get(self):
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return make_response(jsonify(result.data), 200) 

    def post(self):
        user = User(name=request.json['name'], email=request.json['email'])
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return make_response(jsonify(result.data), 200)

    def put(self):
        user = User.query.filter_by(id=request.json['id']).first()
        user.name = request.json['name']
        user.email = request.json['email']
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return make_response(jsonify(result.data), 200) 

class UserById(Resource):
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"status": "success"}), 200) 

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        result = user_schema.dump(user)
        return make_response(jsonify(result.data), 200) 


api.add_resource(Users, '/users') 
api.add_resource(UserById, '/users/<id>') 

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True)

