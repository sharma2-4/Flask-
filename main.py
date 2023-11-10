from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

"""
@app.route("/",methods = ['GET'])
def home():
    return jsonify({'msg':'hello to every one this message from the flask'})
"""
#To find the directory
basedir = os.path.abspath(os.path.dirname(__file__))
#To create the sql file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'db.sqlite')
#To aviod the Warnings
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#To create the table 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

def __init__(self,name,contact):
    self.name = name
    self.contact = contact

#To create the schema 
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','contact')

user_schema = UserSchema() #To add single users
#To create multiple access data
users_schema = UserSchema(many=True)

#To add user using route
@app.route("/user",methods=["POST"])
def add_users():
    name=request.json['name']
    contact=request.json['contact']
    new_user=User(name=name,contact=contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

#To show the all user
@app.route("/user",methods=["GET"])
def getAllUser():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

#TO show the single users
@app.route("/user/<id>",methods=["GET"])
def getAllUserByid(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

#To update 
@app.route("/user/<id>",methods=["PUT"])
def UpdateByid(id):
    user = User.query.get(id)
    name= request.json['name']
    contact=request.json['contact']
    user.name=name
    user.contact=contact
    return user_schema.jsonify(user) 

#To delete the users
@app.route("/user/<id>",methods=['DELETE'])
def DeleteByUser(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == "__main__":
    app.run(debug=True)