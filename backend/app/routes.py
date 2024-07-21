from flask import Blueprint
from flask_jwt_extended import jwt_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Hello, ATS!"

@main.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return "You are viewing a protected route!"
