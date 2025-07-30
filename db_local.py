import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

# Function to connect to SQL Server and print database names
def test_sql_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.tables")
    for row in cursor.fetchall():
        print(row[0])
    conn.close()

def insert_timesheet_entry(date, project, hours, notes):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO dbo.timelogs (Date, Project, Hours, Notes) VALUES (?, ?, ?, ?)',
        (date, project, hours, notes)
    )
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash, role FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_user_by_id(user_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash, role FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def create_user(username, password, role):
    password_hash = generate_password_hash(password)
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, password_hash, role))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash, role, is_confirmed, confirmation_token FROM users WHERE username = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_user_by_token(token):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash, role, is_confirmed, confirmation_token FROM users WHERE confirmation_token = ?', (token,))
    row = cursor.fetchone()
    conn.close()
    return row

def confirm_user(token):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_confirmed = 1, confirmation_token = NULL WHERE confirmation_token = ?', (token,))
    conn.commit()
    conn.close()

def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

def create_project(name, start_date, end_date):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (name, start_date, end_date) OUTPUT INSERTED.id VALUES (?, ?, ?)', (name, start_date, end_date))
    project_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return project_id

def get_all_users():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def assign_users_to_project(project_id, user_ids):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    for user_id in user_ids:
        cursor.execute('INSERT INTO assignments (user_id, project_id) VALUES (?, ?)', (user_id, project_id))
    conn.commit()
    conn.close()

def get_projects_for_user(user_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.name
        FROM projects p
        JOIN assignments a ON p.id = a.project_id
        WHERE a.user_id = ?
    ''', (user_id,))
    projects = cursor.fetchall()
    conn.close()
    return projects

def get_last_project_id():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT SCOPE_IDENTITY()')
    project_id = cursor.fetchone()[0]
    conn.close()
    return project_id

def get_all_projects():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, start_date, end_date FROM projects ORDER BY name')
    projects = cursor.fetchall()
    conn.close()
    return projects

def get_users_for_project(project_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT u.id, u.username, u.role
        FROM users u
        JOIN assignments a ON u.id = a.user_id
        WHERE a.project_id = ?
    ''', (project_id,))
    users = cursor.fetchall()
    conn.close()
    return users

def remove_user_from_project(user_id, project_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('DELETE FROM assignments WHERE user_id = ? AND project_id = ?', (user_id, project_id))
    conn.commit()
    conn.close()

def remove_all_project_assignments(project_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('DELETE FROM assignments WHERE project_id = ?', (project_id,))
    conn.commit()
    conn.close()

def create_task_category(name, description=""):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('INSERT INTO task_categories (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()

def get_all_task_categories():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, description FROM task_categories ORDER BY name')
    categories = cursor.fetchall()
    conn.close()
    return categories

def insert_timesheet_entry_enhanced(user_id, date, project_id, task_category_id, hours, description):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO timesheet_entries (user_id, date, project_id, task_category_id, hours, description, status)
        VALUES (?, ?, ?, ?, ?, ?, 'draft')
    ''', (user_id, date, project_id, task_category_id, hours, description))
    conn.commit()
    conn.close()

def get_timesheet_entries_for_week(user_id, week_start_date):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
               te.hours, te.description, te.status
        FROM timesheet_entries te
        JOIN projects p ON te.project_id = p.id
        JOIN task_categories tc ON te.task_category_id = tc.id
        WHERE te.user_id = ? AND te.date >= ? AND te.date < DATEADD(day, 7, ?)
        ORDER BY te.date, p.name
    ''', (user_id, week_start_date, week_start_date))
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_projects_with_ids_for_user(user_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.name
        FROM projects p
        JOIN assignments a ON p.id = a.project_id
        WHERE a.user_id = ?
        ORDER BY p.name
    ''', (user_id,))
    projects = cursor.fetchall()
    conn.close()
    return projects

def submit_weekly_timesheet(user_id, week_start_date):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE timesheet_entries 
        SET status = 'submitted' 
        WHERE user_id = ? AND date >= ? AND date < DATEADD(day, 7, ?) AND status = 'draft'
    ''', (user_id, week_start_date, week_start_date))
    conn.commit()
    conn.close()

def get_week_total_hours(user_id, week_start_date):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(hours) as total_hours
        FROM timesheet_entries 
        WHERE user_id = ? AND date >= ? AND date < DATEADD(day, 7, ?)
    ''', (user_id, week_start_date, week_start_date))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0

def get_timesheet_entries_for_day(user_id, date):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
               te.hours, te.description, te.status
        FROM timesheet_entries te
        JOIN projects p ON te.project_id = p.id
        JOIN task_categories tc ON te.task_category_id = tc.id
        WHERE te.user_id = ? AND te.date = ?
        ORDER BY p.name
    ''', (user_id, date))
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_day_total_hours(user_id, date):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(hours) as total_hours
        FROM timesheet_entries 
        WHERE user_id = ? AND date = ?
    ''', (user_id, date))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0

def get_timesheet_entries_for_month(user_id, month_start, month_end):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
               te.hours, te.description, te.status
        FROM timesheet_entries te
        JOIN projects p ON te.project_id = p.id
        JOIN task_categories tc ON te.task_category_id = tc.id
        WHERE te.user_id = ? AND te.date >= ? AND te.date <= ?
        ORDER BY te.date, p.name
    ''', (user_id, month_start, month_end))
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_month_total_hours(user_id, month_start, month_end):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(hours) as total_hours
        FROM timesheet_entries 
        WHERE user_id = ? AND date >= ? AND date <= ?
    ''', (user_id, month_start, month_end))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[0] else 0

def update_timesheet_entry(entry_id, user_id, project_id, task_id, description, hours):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    
    try:
        # Update the entry
        cursor.execute('''
            UPDATE timesheet_entries 
            SET project_id = ?, task_category_id = ?, description = ?, hours = ?
            WHERE id = ? AND user_id = ?
        ''', (project_id, task_id, description, hours, entry_id, user_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def delete_timesheet_entry(entry_id, user_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    
    try:
        # Delete the entry
        cursor.execute('''
            DELETE FROM timesheet_entries 
            WHERE id = ? AND user_id = ?
        ''', (entry_id, user_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def update_user_password(user_id, new_password):
    """Update user password"""
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(new_password)
        cursor.execute('''
            UPDATE users 
            SET password_hash = ? 
            WHERE id = ?
        ''', (password_hash, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def get_filtered_entries(start_date, end_date, user_id='', project_id=''):
    """Get filtered entries for admin dashboard"""
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    try:
        query = '''
            SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
                   te.hours, te.description, u.username
            FROM timesheet_entries te
            JOIN projects p ON te.project_id = p.id
            JOIN task_categories tc ON te.task_category_id = tc.id
            JOIN users u ON te.user_id = u.id
            WHERE te.date BETWEEN ? AND ?
        '''
        params = [start_date, end_date]
        
        if user_id:
            query += ' AND te.user_id = ?'
            params.append(user_id)
        
        if project_id:
            query += ' AND te.project_id = ?'
            params.append(project_id)
        
        query += ' ORDER BY te.date DESC, u.username, p.name'
        
        cursor.execute(query, params)
        entries = cursor.fetchall()
        conn.close()
        return entries
    except Exception as e:
        conn.close()
        raise e

def get_user_filtered_entries(user_id, start_date, end_date, project_id=''):
    """Get filtered entries for user dashboard"""
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=GARRY\\SQLEXPRESS;'
        'DATABASE=timesheet;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    try:
        query = '''
            SELECT te.id, te.date, p.name as project_name, tc.name as task_category, 
                   te.hours, te.description
            FROM timesheet_entries te
            JOIN projects p ON te.project_id = p.id
            JOIN task_categories tc ON te.task_category_id = tc.id
            WHERE te.user_id = ? AND te.date BETWEEN ? AND ?
        '''
        params = [user_id, start_date, end_date]
        
        if project_id:
            query += ' AND te.project_id = ?'
            params.append(project_id)
        
        query += ' ORDER BY te.date DESC, p.name'
        
        cursor.execute(query, params)
        entries = cursor.fetchall()
        conn.close()
        return entries
    except Exception as e:
        conn.close()
        raise e

if __name__ == "__main__":
    test_sql_connection()
