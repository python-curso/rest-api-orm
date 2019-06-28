from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

db.drop_all()
db.create_all()    

# Dados iniciais
user = User(name='Nataniel Paiva', email='nataniel.paiva@gmail.com')
db.session.add(user)
db.session.commit()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email")


user_schema = UserSchema()
users_schema = UserSchema(many=True)