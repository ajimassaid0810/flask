from datetime import datetime
from flask import Blueprint, jsonify, request
import requests
from .models import User
from app import db


def fetch_users():
    page = request.args.get('page')

    if not page:
        return jsonify({'message': 'Missing query parameter: page'}), 400

    try:
        # Fetch data from the source URL
        url = f'https://reqres.in/api/users?page={page}'
        response = requests.get(url)
        response_data = response.json()

        if 'data' not in response_data:
            return jsonify({'message': 'Invalid response from the source URL'}), 500

        fetched_users = response_data['data']

        # Check if the fetched data already exists in the database
        existing_user_ids = {user.id for user in User.query.all()}
        new_users = [user for user in fetched_users if user['id'] not in existing_user_ids]

        # Store the new users in the database
        for user_data in new_users:
            new_user = User(
                id=user_data['id'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                avatar=user_data['avatar']
            )
            db.session.add(new_user)

        db.session.commit()

        return jsonify({'message': 'User data fetched and stored successfully', 'data': new_users}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'Error fetching data from the source URL'}), 500

def get_all_users():
    page = request.args.get('page', default=1, type=int)
    items_per_page = request.args.get('per_page', default=6, type=int)

    users = User.query.filter(User.deleted_at == None).paginate(page=page, per_page=items_per_page)

    if not users.items:
        return jsonify({'message': 'No users found'}), 404

    result = []
    for user in users.items:
        result.append({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.avatar
        })

    response = {
        "page": page,
        "per_page": items_per_page,
        "total": users.total,
        "total_pages": users.pages,
        "data": result
    }

    return jsonify(response), 200
    

def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    elif user.deleted_at is not None:
        return jsonify({'message': 'User has been deleted'}), 410  
    else:
        return jsonify({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar': user.avatar,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'deleted_at': user.deleted_at
        }), 200
    

def add_user():
    try:
        data = request.get_json()
        if not request.is_json:
            return jsonify({'message': 'Invalid Content-Type. Please send JSON data.'}), 400

        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        avatar = data.get('avatar')

        if not email or not first_name or not last_name:
            return jsonify({'message': 'Please provide email, first name, and last name'}), 400

        new_user = User(email=email, first_name=first_name, last_name=last_name, avatar=avatar)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User added successfully', 'created_at': new_user.created_at}), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'message': 'An error occurred. Please check your request data.'}), 500

def update_user(user_id):
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    avatar = data.get('avatar')

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if avatar:
        user.avatar = avatar

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

def delete_user(user_id):
    authorization_header = request.headers.get('Authorization')
    if authorization_header != 'Bearer 3cdcnTiBsl':
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.deleted_at = datetime.utcnow()
    db.session.commit()
    db.session.close() 

    return jsonify({'message': 'User deleted successfully'}), 200