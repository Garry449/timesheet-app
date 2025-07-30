import db

# Create admin user
db.create_user('admin', 'admin', 'admin')
print("Admin user created successfully!")
print("Username: admin")
print("Password: admin")
print("Role: admin") 