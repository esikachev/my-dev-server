from flask import Flask
from flask import jsonify
from flask import request

from sqlalchemy import exists

from my_dev_server.db import base
from my_dev_server.db import models

app = Flask(__name__)


@app.route('/users', methods=['POST'])
def login():
    if request.method == 'POST':
        # POST request for creating user
        new_user = models.User(username=request.json["username"],
                               email=request.json['email'])

        user_exist = (
            models.User.query.filter_by(username=new_user.username).all() or
            models.User.query.filter_by(email=new_user.email).all())

        if not user_exist:
            base.session.add(new_user)
            base.session.commit()
            return jsonify(new_user.to_json())
        else:
            return('User exists')


@app.route('/users/<id>', methods=['GET', 'DELETE'])
def user_changes(id):
    if request.method == 'GET':
        user = models.User.query.filter_by(id=id).first()
        return jsonify(user.to_json())
    if request.method == 'DELETE':
        models.User.query.filter_by(id=id).delete()
        base.session.commit()


def main():
    app.run(debug=True)

