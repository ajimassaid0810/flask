from flask import Blueprint, jsonify, request
# from .user.controller import fetch_users, get_all_users, get_user, add_user, update_user, delete_user
from .helth.controller import predict
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Welcome to Akasia Test!'

bp.route('/predict', methods=['POST'])(predict)