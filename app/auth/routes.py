"""
Authentication Routes
=====================
API endpoints for user authentication including registration and login.

Endpoints:
- POST /auth/register - Register a new user
- POST /auth/login - Authenticate and get JWT token
- GET /auth/profile - Get current user profile
- POST /auth/refresh - Refresh JWT token
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from app import db
from app.models import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a New User
    
    Creates a new user account with the provided credentials and attributes.
    
    Request Body (JSON):
        {
            "username": "string (required)",
            "email": "string (required)",
            "password": "string (required)",
            "role": "string (optional, default: 'employee')",
            "department": "string (optional, default: 'general')",
            "designation": "string (optional)"
        }
    
    Returns:
        201: User created successfully
        400: Validation error
        409: Username or email already exists
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Request body is required'
        }), 400
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'status': 'error',
                'message': f'{field} is required'
            }), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'status': 'error',
            'message': 'Username already exists'
        }), 409
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'status': 'error',
            'message': 'Email already exists'
        }), 409
    
    # Validate password strength
    if len(data['password']) < 6:
        return jsonify({
            'status': 'error',
            'message': 'Password must be at least 6 characters'
        }), 400
    
    # Validate role
    valid_roles = ['admin', 'manager', 'employee']
    role = data.get('role', 'employee').lower()
    if role not in valid_roles:
        return jsonify({
            'status': 'error',
            'message': f'Invalid role. Must be one of: {", ".join(valid_roles)}'
        }), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        role=role,
        department=data.get('department', 'general').lower(),
        designation=data.get('designation')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict()
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Registration failed: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User Login
    
    Authenticates user and returns a JWT access token.
    The token contains user attributes for OPA policy evaluation.
    
    Request Body (JSON):
        {
            "username": "string (required)",
            "password": "string (required)"
        }
    
    Returns:
        200: Login successful with JWT token
        400: Missing credentials
        401: Invalid credentials
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Request body is required'
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': 'Username and password are required'
        }), 400
    
    # Find user by username
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({
            'status': 'error',
            'message': 'Invalid username or password'
        }), 401
    
    if not user.is_active:
        return jsonify({
            'status': 'error',
            'message': 'Account is deactivated'
        }), 401
    
    # Create JWT token with user attributes as additional claims
    # These claims are used by OPA for policy evaluation
    additional_claims = {
        'role': user.role,
        'department': user.department,
        'designation': user.designation,
        'username': user.username
    }
    
    access_token = create_access_token(
        identity=user.id,
        additional_claims=additional_claims
    )
    
    return jsonify({
        'status': 'success',
        'message': 'Login successful',
        'data': {
            'access_token': access_token,
            'token_type': 'Bearer',
            'user': user.to_dict()
        }
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get Current User Profile
    
    Returns the profile of the currently authenticated user.
    Requires a valid JWT token in the Authorization header.
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: User profile data
        401: Invalid or missing token
        404: User not found
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': {
            'user': user.to_dict()
        }
    }), 200


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """
    List All Users (Admin Only)
    
    Returns a list of all registered users.
    Only accessible by admin users.
    
    Returns:
        200: List of users
        403: Access denied (non-admin)
    """
    jwt_claims = get_jwt()
    
    if jwt_claims.get('role') != 'admin':
        return jsonify({
            'status': 'error',
            'message': 'Admin access required'
        }), 403
    
    users = User.query.all()
    
    return jsonify({
        'status': 'success',
        'data': {
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }
    }), 200


@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update User (Admin Only)
    
    Updates user attributes. Only accessible by admin users.
    
    Args:
        user_id: ID of user to update
    
    Request Body (JSON):
        {
            "role": "string (optional)",
            "department": "string (optional)",
            "designation": "string (optional)",
            "is_active": "boolean (optional)"
        }
    
    Returns:
        200: User updated successfully
        403: Access denied
        404: User not found
    """
    jwt_claims = get_jwt()
    
    if jwt_claims.get('role') != 'admin':
        return jsonify({
            'status': 'error',
            'message': 'Admin access required'
        }), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    data = request.get_json()
    
    # Update allowed fields
    if 'role' in data:
        valid_roles = ['admin', 'manager', 'employee']
        if data['role'].lower() in valid_roles:
            user.role = data['role'].lower()
    
    if 'department' in data:
        user.department = data['department'].lower()
    
    if 'designation' in data:
        user.designation = data['designation']
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'User updated successfully',
            'data': {
                'user': user.to_dict()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Update failed: {str(e)}'
        }), 500
