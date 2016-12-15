
from my_dev_server.db.models import User, Ssh
from flask import Flask, request, jsonify

from sqlalchemy import exists

from my_dev_server.db.base import session

app = Flask(__name__)


@app.route('/users', methods=['POST'])
def login():
    if request.method == 'POST':
        #POST request for creating user
        new_user = User(username=request.json["username"],
                        email=request.json['email'])

        user_exist = (
            User.query.filter_by(username=new_user.username).all() or
            User.query.filter_by(email=new_user.email).all())

        if not user_exist:
            session.add(new_user)
            session.commit()
            return jsonify(new_user.to_json())
        else:
            return('User exists')


@app.route('/users/<id>', methods=['GET', 'POST', 'DELETE'])
def user_changes(id):
    if request.method == 'POST':
        # POST request for updating user
        new_user = User(username=request.json["username"],
                        email=request.json['email'])
        if new_user.username in User.query.all():
            session.add(new_user)
            session.commit()
        return str(new_user.id)
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        return jsonify(user.to_json())
    if request.method == 'DELETE':
        User.query.filter_by(id=id).delete()
        session.commit()


def main():
    app.run(debug=True)

