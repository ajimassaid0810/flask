from flask import Blueprint, jsonify, request
from .user.controller import fetch_users, get_all_users, get_user, add_user, update_user, delete_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Welcome to Akasia Test!'

bp.route('/user/fetch', methods=['GET'])(fetch_users)
bp.route('/users', methods=['GET'])(get_all_users)
bp.route('/user/<int:user_id>', methods=['GET'])(get_user)
bp.route('/user', methods=['POST'])(add_user)
bp.route('/user/<int:user_id>', methods=['PUT'])(update_user)
bp.route('/user/<int:user_id>', methods=['DELETE'])(delete_user)
