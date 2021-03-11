from flask import Blueprint, render_template

user = Blueprint('user', __name__)


@user.route('/register')
def register():
    return "register"


@user.route('/register', methods=['POST'])
def register_submit():
    return "submit"


@user.route('/login', methods=['POST'])
def login():
    return "login"