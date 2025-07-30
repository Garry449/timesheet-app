"""
Simplified database adapter for cloud deployment
Uses pure Python PostgreSQL adapter (pg8000) for better compatibility
"""

import os
import pg8000
from datetime import datetime, timedelta

def get_connection():
    """Get database connection"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return pg8000.connect(database_url)
    else:
        # Fallback for local testing
        return pg8000.connect(
            host='localhost',
            database='timesheet',
            user='postgres',
            password='password'
        )

def get_user_by_username(username):
    """Get user by username"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = %s', (username,))
        row = cursor.fetchone()
        return row
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, username, password_hash, role FROM users WHERE id = %s', (user_id,))
        row = cursor.fetchone()
        return row
    finally:
        conn.close()

def verify_password(password_hash, password):
    """Verify password"""
    from werkzeug.security import check_password_hash
    return check_password_hash(password_hash, password)

def get_projects_with_ids_for_user(user_id):
    """Get projects for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT p.id, p.name 
            FROM projects p 
            JOIN user_projects up ON p.id = up.project_id 
            WHERE up.user_id = %s
        ''', (user_id,))
        projects = cursor.fetchall()
        return projects
    finally:
        conn.close()

def get_all_task_categories():
    """Get all task categories"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, name FROM task_categories ORDER BY name')
        categories = cursor.fetchall()
        return categories
    finally:
        conn.close()

def insert_timesheet_entry_enhanced(user_id, date, project_id, task_category_id, hours, description):
    """Insert timesheet entry"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO timesheet_entries (user_id, date, project_id, task_category_id, hours, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending')
        ''', (user_id, date, project_id, task_category_id, hours, description))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error inserting timesheet entry: {e}")
        return False
    finally:
        conn.close()

def get_timesheet_entries_for_week(user_id, start_date, end_date):
    """Get timesheet entries for a week"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
                   te.hours, te.description, te.status
            FROM timesheet_entries te
            JOIN projects p ON te.project_id = p.id
            JOIN task_categories tc ON te.task_category_id = tc.id
            WHERE te.user_id = %s AND te.date BETWEEN %s AND %s
            ORDER BY te.date, te.id
        ''', (user_id, start_date, end_date))
        entries = cursor.fetchall()
        return entries
    finally:
        conn.close()

def get_timesheet_entries_for_month(user_id, year, month):
    """Get timesheet entries for a month"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
                   te.hours, te.description, te.status
            FROM timesheet_entries te
            JOIN projects p ON te.project_id = p.id
            JOIN task_categories tc ON te.task_category_id = tc.id
            WHERE te.user_id = %s AND EXTRACT(YEAR FROM te.date) = %s AND EXTRACT(MONTH FROM te.date) = %s
            ORDER BY te.date, te.id
        ''', (user_id, year, month))
        entries = cursor.fetchall()
        return entries
    finally:
        conn.close()

def get_timesheet_entries_for_day(user_id, date):
    """Get timesheet entries for a specific day"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
                   te.hours, te.description, te.status
            FROM timesheet_entries te
            JOIN projects p ON te.project_id = p.id
            JOIN task_categories tc ON te.task_category_id = tc.id
            WHERE te.user_id = %s AND te.date = %s
            ORDER BY te.id
        ''', (user_id, date))
        entries = cursor.fetchall()
        return entries
    finally:
        conn.close()

def update_timesheet_entry(entry_id, project_id, task_category_id, hours, description):
    """Update timesheet entry"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE timesheet_entries 
            SET project_id = %s, task_category_id = %s, hours = %s, description = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        ''', (project_id, task_category_id, hours, description, entry_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error updating timesheet entry: {e}")
        return False
    finally:
        conn.close()

def delete_timesheet_entry(entry_id):
    """Delete timesheet entry"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM timesheet_entries WHERE id = %s', (entry_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error deleting timesheet entry: {e}")
        return False
    finally:
        conn.close()

# Add other necessary functions as needed
def get_all_users():
    """Get all users"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, username, role FROM users ORDER BY username')
        users = cursor.fetchall()
        return users
    finally:
        conn.close()

def get_all_projects():
    """Get all projects"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, name, start_date, end_date FROM projects ORDER BY name')
        projects = cursor.fetchall()
        return projects
    finally:
        conn.close()

def create_project(name, start_date, end_date):
    """Create a new project"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO projects (name, start_date, end_date) 
            VALUES (%s, %s, %s) RETURNING id
        ''', (name, start_date, end_date))
        project_id = cursor.fetchone()[0]
        conn.commit()
        return project_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating project: {e}")
        return None
    finally:
        conn.close()

def assign_users_to_project(project_id, user_ids):
    """Assign users to a project"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for user_id in user_ids:
            cursor.execute('''
                INSERT INTO user_projects (user_id, project_id) 
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            ''', (user_id, project_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error assigning users to project: {e}")
        return False
    finally:
        conn.close()

def remove_all_project_assignments(project_id):
    """Remove all user assignments for a project"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM user_projects WHERE project_id = %s', (project_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error removing project assignments: {e}")
        return False
    finally:
        conn.close()

def update_user_password(user_id, new_password_hash):
    """Update user password"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET password_hash = %s WHERE id = %s', (new_password_hash, user_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error updating user password: {e}")
        return False
    finally:
        conn.close() 