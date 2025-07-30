import os
import pg8000
import pyodbc
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self):
        self.db_type = os.environ.get('DATABASE_TYPE', 'sqlserver')  # 'sqlserver' or 'postgresql'
        
    def get_connection(self):
        """Get database connection based on environment"""
        if self.db_type == 'postgresql':
            return self._get_postgresql_connection()
        else:
            return self._get_sqlserver_connection()
    
    def _get_postgresql_connection(self):
        """Get PostgreSQL connection for cloud deployment"""
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            return pg8000.connect(database_url)
        else:
            # Fallback to local PostgreSQL (for testing)
            return pg8000.connect(
                host='localhost',
                database='timesheet',
                user='postgres',
                password='password'
            )
    
    def _get_sqlserver_connection(self):
        """Get SQL Server connection for local development"""
        return pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=GARRY\\SQLEXPRESS;'
            'DATABASE=timesheet;'
            'Trusted_Connection=yes;'
        )

# Create global database manager instance
db_manager = DatabaseManager()

# Import all existing functions from db.py and adapt them
# This is a simplified version - you'll need to adapt all your existing functions

def get_user_by_username(username):
    """Get user by username - works with both SQL Server and PostgreSQL"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    if db_manager.db_type == 'postgresql':
        cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = %s', (username,))
    else:
        cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
    
    row = cursor.fetchone()
    conn.close()
    return row

def verify_password(password_hash, password):
    """Verify password - works with both databases"""
    from werkzeug.security import check_password_hash
    return check_password_hash(password_hash, password)

def get_projects_with_ids_for_user(user_id):
    """Get projects for user - works with both databases"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    if db_manager.db_type == 'postgresql':
        cursor.execute('''
            SELECT p.id, p.name 
            FROM projects p 
            JOIN user_projects up ON p.id = up.project_id 
            WHERE up.user_id = %s
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT p.id, p.name 
            FROM projects p 
            JOIN user_projects up ON p.id = up.project_id 
            WHERE up.user_id = ?
        ''', (user_id,))
    
    projects = cursor.fetchall()
    conn.close()
    return projects

def get_all_task_categories():
    """Get all task categories - works with both databases"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    if db_manager.db_type == 'postgresql':
        cursor.execute('SELECT id, name FROM task_categories ORDER BY name')
    else:
        cursor.execute('SELECT id, name FROM task_categories ORDER BY name')
    
    categories = cursor.fetchall()
    conn.close()
    return categories

def insert_timesheet_entry_enhanced(user_id, date, project_id, task_category_id, hours, description):
    """Insert timesheet entry - works with both databases"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    try:
        if db_manager.db_type == 'postgresql':
            cursor.execute('''
                INSERT INTO timesheet_entries (user_id, date, project_id, task_category_id, hours, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            ''', (user_id, date, project_id, task_category_id, hours, description))
        else:
            cursor.execute('''
                INSERT INTO timesheet_entries (user_id, date, project_id, task_category_id, hours, description, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            ''', (user_id, date, project_id, task_category_id, hours, description))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error inserting timesheet entry: {e}")
        return False

# Add more functions as needed...
# You'll need to adapt all your existing db.py functions to work with both databases 