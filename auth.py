# auth.py
"""
Authentication and user management module
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(UserMixin):
    """User model for authentication"""
    
    def __init__(self, username, email, role='user', password_hash=None, _id=None, created_at=None):
        self.username = username
        self.email = email
        self.role = role  # 'admin' or 'user'
        self.password_hash = password_hash
        self._id = _id
        self.created_at = created_at or datetime.now()
    
    def get_id(self):
        """Required by Flask-Login"""
        return str(self._id)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def to_dict(self):
        """Convert user to dictionary for MongoDB"""
        return {
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'password_hash': self.password_hash,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create User from MongoDB document"""
        return User(
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role', 'user'),
            password_hash=data.get('password_hash'),
            _id=data.get('_id'),
            created_at=data.get('created_at')
        )


class UserManager:
    """Manage users in MongoDB"""
    
    def __init__(self, mongo_handler):
        self.mongo = mongo_handler
        self.collection_name = 'users'
    
    def get_collection(self):
        """Get users collection"""
        if self.mongo.is_connected():
            return self.mongo.db[self.collection_name]
        return None
    
    def create_user(self, username, email, password, role='user'):
        """Create a new user"""
        collection = self.get_collection()
        if not collection:
            return False, "Database not connected"
        
        # Check if username already exists
        if collection.find_one({'username': username}):
            return False, "Username already exists"
        
        # Check if email already exists
        if collection.find_one({'email': email}):
            return False, "Email already exists"
        
        # Create user
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        # Insert into database
        result = collection.insert_one(user.to_dict())
        user._id = result.inserted_id
        
        return True, user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        collection = self.get_collection()
        if not collection:
            return None
        
        try:
            user_data = collection.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return User.from_dict(user_data)
        except:
            pass
        return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        collection = self.get_collection()
        if not collection:
            return None
        
        user_data = collection.find_one({'username': username})
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        collection = self.get_collection()
        if not collection:
            return None
        
        user_data = collection.find_one({'email': email})
        if user_data:
            return User.from_dict(user_data)
        return None
    
    def get_all_users(self):
        """Get all users"""
        collection = self.get_collection()
        if not collection:
            return []
        
        users = []
        for user_data in collection.find():
            users.append(User.from_dict(user_data))
        return users
    
    def update_user(self, user_id, **kwargs):
        """Update user fields"""
        collection = self.get_collection()
        if not collection:
            return False
        
        update_data = {}
        if 'email' in kwargs:
            update_data['email'] = kwargs['email']
        if 'role' in kwargs:
            update_data['role'] = kwargs['role']
        if 'password' in kwargs:
            update_data['password_hash'] = generate_password_hash(kwargs['password'])
        
        if update_data:
            try:
                collection.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$set': update_data}
                )
                return True
            except:
                pass
        return False
    
    def delete_user(self, user_id):
        """Delete user"""
        collection = self.get_collection()
        if not collection:
            return False
        
        try:
            result = collection.delete_one({'_id': ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def user_exists(self):
        """Check if any user exists in database"""
        collection = self.get_collection()
        if not collection:
            return False
        return collection.count_documents({}) > 0
    
    def create_default_admin(self):
        """Create default admin user if no users exist"""
        if not self.user_exists():
            success, user = self.create_user(
                username='admin',
                email='admin@cashrecon.com',
                password='admin123',
                role='admin'
            )
            if success:
                print("✓ Default admin user created")
                print("  Username: admin")
                print("  Password: admin123")
                print("  ⚠️  PLEASE CHANGE THE PASSWORD AFTER FIRST LOGIN!")
                return True
        return False
