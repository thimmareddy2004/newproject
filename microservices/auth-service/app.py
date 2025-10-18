import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, url_for, flash
from shared.database import db, User, LoginTracking, init_db
from shared.config import config
from datetime import datetime

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    init_db(app)
    
    return app

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "auth-service"})

@app.route('/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"ok": False, "error": "JSON data required"}), 400
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        
        # Validation
        if not email:
            return jsonify({"ok": False, "error": "Email is required"}), 400
        if not password:
            return jsonify({"ok": False, "error": "Password is required"}), 400
        if not first_name:
            return jsonify({"ok": False, "error": "First name is required"}), 400
        if not last_name:
            return jsonify({"ok": False, "error": "Last name is required"}), 400
            
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"ok": False, "error": "Email already registered"}), 409
        
        # Create new user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=data.get('phone', ''),
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "ok": True, 
            "message": "Account created successfully",
            "user": user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/signin', methods=['POST'])
def signin():
    """User login endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"ok": False, "error": "JSON data required"}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"ok": False, "error": "Email and password required"}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"ok": False, "error": "Invalid email or password"}), 401
        
        # Record login event
        login_entry = LoginTracking(user_id=user.id)
        db.session.add(login_entry)
        db.session.commit()
        
        return jsonify({
            "ok": True,
            "message": "Login successful",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user information"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"ok": False, "error": "User not found"}), 404
        
        return jsonify({
            "ok": True,
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/admin/logins', methods=['GET'])
def admin_get_logins():
    """Get all login records for admin"""
    try:
        # Fetch all logins with user info ordered by login_time desc
        logins = LoginTracking.query.join(User).order_by(LoginTracking.login_time.desc()).all()
        
        login_data = []
        for login in logins:
            login_data.append({
                "id": login.id,
                "user_id": login.user_id,
                "user_name": f"{login.user.first_name} {login.user.last_name}",
                "user_email": login.user.email,
                "login_time": login.login_time.isoformat() if login.login_time else None
            })
        
        return jsonify({
            "ok": True,
            "logins": login_data
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)