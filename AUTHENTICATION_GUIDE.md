# 🔐 Authentication System Documentation

## Overview

Your Cash Reconciliation app now includes a complete authentication system with:
- ✅ **Login/Logout** functionality
- ✅ **User Management** (Admin only)
- ✅ **Role-Based Access Control** (Admin vs User)
- ✅ **Password Security** (hashed passwords)
- ✅ **MongoDB Storage** (users stored in database)

---

## 🚀 Features

### 1. **Login System**
- Beautiful login page
- Secure password authentication
- Session management
- Remember user across requests

### 2. **Role-Based Access**
- **Admin Users:**
  - Can access all features
  - Can add new users
  - Can delete users
  - Can manage user roles
  - Access to user management dashboard

- **Regular Users:**
  - Can access reconciliation features
  - Cannot manage users
  - Can change own password

### 3. **User Management Dashboard**
- Add new users
- Delete users
- View all users
- Change passwords
- Assign roles (Admin/User)

### 4. **Security Features**
- Passwords are hashed (bcrypt)
- Protected routes require login
- Admin-only routes protected
- Session management
- CSRF protection

---

## 📋 Default Admin Credentials

When you first deploy the app, a default admin account is automatically created:

```
Username: admin
Password: admin123
```

**⚠️ IMPORTANT:** Change this password immediately after first login!

---

## 🎯 Quick Start

### Step 1: Deploy Your App
Deploy as normal (Railway/Dokploy). The authentication system is already integrated.

### Step 2: First Login
1. Visit your app URL
2. You'll see the login page
3. Use default credentials:
   - Username: `admin`
   - Password: `admin123`

### Step 3: Change Default Password
1. After logging in, click **"Manage Users"**
2. Scroll to **"Change Your Password"** section
3. Enter current password: `admin123`
4. Enter new secure password
5. Click **"Update Password"**

### Step 4: Add Team Members
1. In User Management, fill out the **"Add New User"** form:
   - Username
   - Email
   - Password
   - Role (User or Admin)
2. Click **"Create User"**
3. Share credentials with team member

---

## 👥 User Roles Explained

### Admin Role
Admins have full access to everything:
- ✅ Upload files
- ✅ Process reconciliation
- ✅ Export reports
- ✅ **Manage users** (add, delete)
- ✅ **Assign roles**
- ✅ Change passwords

**Use case:** Managers, supervisors, system administrators

### User Role
Regular users can only:
- ✅ Upload files
- ✅ Process reconciliation
- ✅ Export reports
- ✅ Change own password
- ❌ Cannot manage other users

**Use case:** Staff members, analysts

---

## 🎨 User Interface

### Login Page
- Clean, modern design
- Shows default credentials on first launch
- Error messages for invalid login
- Mobile-responsive

### Navigation Bar
Once logged in, you'll see:
- Your username and role
- **"Manage Users"** button (Admin only)
- **"Logout"** button

### User Management Dashboard (Admin Only)
- **Add User Form:** Create new accounts
- **User List Table:** View all users
- **Delete Button:** Remove users
- **Change Password:** Update your password

---

## 🔧 How It Works

### Database Structure
Users are stored in MongoDB in the `users` collection:

```javascript
{
  "_id": ObjectId("..."),
  "username": "john_doe",
  "email": "john@company.com",
  "password_hash": "$2b$12$...",  // Hashed, never plain text
  "role": "user",  // or "admin"
  "created_at": ISODate("2025-12-08...")
}
```

### Authentication Flow

```
User visits app
    ↓
Not logged in? → Redirect to /login
    ↓
Enter credentials
    ↓
Check username & password
    ↓
Valid? → Create session → Redirect to reconciliation
    ↓
Invalid? → Show error message
```

### Protected Routes

All important routes are protected with `@login_required`:
- `/` - Main reconciliation page
- `/upload_files` - File upload
- `/process_recon` - Process reconciliation
- `/export_recon` - Export to Excel
- `/admin/users` - User management (Admin only)

---

## 🛡️ Security Best Practices

### 1. Change Default Password
**Immediately** after first login, change the default admin password.

### 2. Use Strong Passwords
- Minimum 6 characters (enforced)
- Use mix of letters, numbers, symbols
- Avoid common passwords

### 3. Limit Admin Accounts
- Only give Admin role to trusted users
- Most users should have "User" role

### 4. Regular Password Changes
- Change passwords periodically
- Change immediately if compromised

### 5. Delete Unused Accounts
- Remove users who leave the organization
- Audit user list regularly

---

## 📖 Usage Examples

### Example 1: Adding a New User

**As Admin:**
1. Click **"Manage Users"** in top navigation
2. Fill out the form:
   - Username: `sarah_analyst`
   - Email: `sarah@company.com`
   - Password: `SecurePass123!`
   - Role: `User`
3. Click **"Create User"**
4. Share credentials with Sarah

### Example 2: Deleting a User

**As Admin:**
1. Go to User Management
2. Find user in the table
3. Click **"Delete"** button
4. Confirm deletion

### Example 3: Promoting User to Admin

Currently, to change a user's role:
1. Delete the user
2. Re-create with Admin role

Or you can update the database directly in MongoDB Atlas.

### Example 4: Changing Your Password

**Any User:**
1. Go to User Management (or just the page if regular user)
2. Scroll to **"Change Your Password"**
3. Enter current password
4. Enter new password (min 6 characters)
5. Click **"Update Password"**

---

## 🔍 Troubleshooting

### Issue: "Can't login with default credentials"

**Solution:**
1. Check MongoDB Atlas is connected
2. Restart the app to create default admin
3. Check logs for "Default admin user created" message
4. If still failing, manually create admin in MongoDB

### Issue: "Access denied" when clicking Manage Users

**Solution:**
1. You must be logged in as Admin
2. Check your role in User Management
3. Default admin account has Admin role

### Issue: "Forgot password"

**Solution:**
Since there's no password reset yet, you have two options:
1. **Admin can recreate account:**
   - Delete old user
   - Create new user with same username
2. **Direct MongoDB edit:**
   - Access MongoDB Atlas
   - Update password_hash field

### Issue: "Session expired"

**Solution:**
- Flask sessions expire after inactivity
- Just log in again
- Your work is saved in MongoDB

---

## 🚀 Advanced: Manual Database Operations

### Create Admin User via MongoDB

If you need to manually create an admin:

1. Go to MongoDB Atlas
2. Browse Collections → `users`
3. Insert Document:

```javascript
{
  "username": "new_admin",
  "email": "admin@company.com",
  "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5BoKVmVWj.0Gi",
  // This is hash for "admin123"
  "role": "admin",
  "created_at": new Date()
}
```

### View All Users

In MongoDB Atlas:
1. Browse Collections
2. Select `users` collection
3. View all user documents

### Delete User

In MongoDB Atlas:
1. Find user in `users` collection
2. Click trash icon
3. Confirm deletion

---

## 📊 MongoDB Collections

Your app now uses these collections:

1. **users** - User accounts and authentication
2. **session_rec** - Reconciliation data
3. **carry_forward** - Unmatched items
4. **history** - Historical matches
5. **accounts** - Account list
6. **session_metadata** - Session info

---

## 🎓 For Developers

### Adding New Roles

Edit `auth.py` to add new roles:

```python
# Add new role check
def is_manager(self):
    return self.role == 'manager'
```

### Custom Decorators

Create custom decorators for new roles:

```python
def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not current_user.is_manager():
            return "Access denied", 403
        return f(*args, **kwargs)
    return decorated_function
```

### Adding Password Reset

To add password reset functionality:
1. Add email sending capability
2. Generate reset tokens
3. Create reset password form
4. Add route to handle reset

---

## 📝 Files Added/Modified

### New Files:
- `auth.py` - Authentication module
- `templates/login.html` - Login page
- `templates/admin_users.html` - User management page

### Modified Files:
- `app_with_mongodb.py` → `app_with_auth.py` - Added authentication
- `templates/reconciliation.html` - Added user info & logout
- `requirements.txt` - Added Flask-Login

---

## ✅ Testing Checklist

After deploying with authentication:

- [ ] Can access login page
- [ ] Can login with admin/admin123
- [ ] See user info in navigation
- [ ] Can access reconciliation features
- [ ] Can click "Manage Users" (Admin)
- [ ] Can add new user
- [ ] Can delete user
- [ ] Can change password
- [ ] Can logout
- [ ] New user can login
- [ ] Regular user cannot access Manage Users
- [ ] Logout works properly

---

## 🎉 Summary

Your app now has enterprise-grade authentication:
- ✅ Secure login system
- ✅ Role-based access control
- ✅ User management dashboard
- ✅ Password hashing
- ✅ Session management
- ✅ Admin-only features
- ✅ Professional UI

**Default Login:**
- Username: `admin`
- Password: `admin123`

**Remember:** Change default password after first login!

---

## 📞 Support

If you have issues with authentication:
1. Check MongoDB is connected
2. Check logs for errors
3. Verify default admin was created
4. Test with default credentials first

---

**Last Updated:** December 8, 2025
**Version:** 2.0 with Authentication
