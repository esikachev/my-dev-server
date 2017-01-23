from flask import Flask
from flask import jsonify
from flask import request
from sqlalchemy import exists
from sqlalchemy import or_
from oslo_config import cfg

from my_dev_server.db import base
from my_dev_server import config
from my_dev_server.db import models
from my_dev_server import logger

LOG = logger.logger


config.parse_config()
CONF = cfg.CONF

mydev = Flask(__name__)

USER_EXIST_MSG = "User exist"
SSH_EXIST_MSG = "SSH exist"


@mydev.route('/users', methods=['POST'], strict_slashes=False)
def user_create():
    LOG.info('%s %s %s %s' % (str(request.method),
                              str(request.json["username"]),
                              str(request.json["email"]),
                              str(request.json["password"])))
    new_user = models.User(username=request.json["username"],
                           email=request.json['email'],
                           password=request.json["password"])

    username_exist = (
        models.User.query.filter_by(username=new_user.username).all())
    email_exist = (
        models.User.query.filter_by(email=new_user.email).all())

    if username_exist:
        error_msg = "%s with username: %s" % (USER_EXIST_MSG,
                                              request.json["username"])
        LOG.error(error_msg)
        return error_msg

    if email_exist:
        error_msg = "%s with email: %s" % (USER_EXIST_MSG,
                                           request.json["email"])
        LOG.error(error_msg)
        return error_msg

    base.session.add(new_user)
    base.session.commit()
    user_json = jsonify(new_user.to_json())
    LOG.info("Created user %s" % str(user_json))
    return user_json


@mydev.route('/users/<id>', methods=['GET'], strict_slashes=False)
def user_get(id):
    LOG.info('%s %s' % (request.method, id))
    user = models.User.query.filter(or_(models.User.id == key,
                                        models.User.username == key)).first()
    if user is None:
        error_msg = "User with id %s does not exist" % id
        LOG.error(error_msg)
        return error_msg
    return jsonify(user.to_json())


@mydev.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def user_delete(id):
    LOG.info('%s %s' % (request.method, id))
    user = models.User.query.filter_by(id=id).first()
    if user is None:
        error_msg = "Can not delete user %s: it does't exist" % id
        LOG.error(error_msg)
        return error_msg
    models.User.query.filter_by(id=id).delete()
    base.session.commit()
    return '200'


@mydev.route('/users/<user_id>/ssh', methods=['POST'], strict_slashes=False)
def create_ssh(user_id):
    new_ssh = models.Ssh(
        user_id=user_id,
        username=request.json['username'],
        password=request.json['password'],
        alias=request.json['alias'],
        host=request.json['host'])

    # TODO (imenkov) here need to add checking that user authorized
    ssh_exist = models.Ssh.query.filter_by(
        host=new_ssh.host,
        username=new_ssh.username).all()

    if ssh_exist:
        error_msg = "%s with username: %s" % (SSH_EXIST_MSG,
                                              request.json["username"])
        LOG.error(error_msg)
        return error_msg

    base.session.add(new_ssh)
    base.session.commit()

    return jsonify(new_ssh.to_json())


@mydev.route('/users/<user_id>/ssh/<ssh_id>',
             methods=['GET'], strict_slashes=False)
def ssh_get(user_id, ssh_id):
    # TODO (imenkov) here need to add checking that user authorized
    LOG.info('%s %s' % (request.method, ssh_id))
    ssh = models.Ssh.query.filter_by(
        user_id=user_id,
        id=ssh_id).first()

    return jsonify(ssh.to_json())


@mydev.route('/users/<user_id>/ssh/<ssh_id>',
             methods=['DELETE'], strict_slashes=False)
def ssh_delete(user_id, ssh_id):
    # TODO (imenkov) here need to add checking that user authorized
    LOG.info('%s %s' % (request.method, ssh_id))
    models.Ssh.query.filter_by(user_id=user_id,
                               id=ssh_id).delete()
    base.session.commit()
    return '200'


def main():
    mydev.run(debug=CONF.debug, host=CONF.host)

