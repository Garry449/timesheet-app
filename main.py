from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os

# Use cloud database if DATABASE_URL is set (production/cloud), otherwise use local db
if os.environ.get('DATABASE_URL'):
    import db_cloud as db
    print("Using cloud database (PostgreSQL)")
else:
    import db_local as db
    print("Using local database (SQL Server)")

from datetime import datetime, timedelta
import calendar
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_mail import Mail, Message
import uuid
import os
import json
from functools import wraps
import csv
from io import StringIO
from flask import Response

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def get(username):
        row = db.get_user_by_username(username)
        if row:
            return User(*row)
        return None

@login_manager.user_loader
def load_user(user_id):
    row = db.get_user_by_id(user_id)
    if row:
        return User(*row[:4])
    return None

# Flask-Mail config (fill with your SMTP credentials)
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
mail = Mail(app)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.username != 'admin':
            flash('Access denied. Admin privileges required.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/projects', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_projects():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        selected_users = request.form.getlist('users')
        
        # Create project and get the project ID
        project_id = db.create_project(name, start_date, end_date)
        
        # Assign users to the project
        if selected_users:
            db.assign_users_to_project(project_id, selected_users)
        
        flash('Project created and users assigned successfully!')
        return redirect(url_for('admin_projects'))
    
    users = db.get_all_users()
    return render_template('admin_projects.html', users=users)

@app.route('/admin/project-list')
@login_required
@admin_required
def admin_project_list():
    projects = db.get_all_projects()
    return render_template('admin_project_list.html', projects=projects)

@app.route('/admin/assign-users/<int:project_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_assign_users(project_id):
    if request.method == 'POST':
        selected_users = request.form.getlist('users')
        
        # Remove existing assignments for this project
        db.remove_all_project_assignments(project_id)
        
        # Assign new users
        if selected_users:
            db.assign_users_to_project(project_id, selected_users)
        
        flash('Users assigned to project successfully!')
        return redirect(url_for('admin_project_list'))
    
    all_users = db.get_all_users()
    assigned_users = db.get_users_for_project(project_id)
    assigned_user_ids = [user[0] for user in assigned_users]
    
    return render_template('admin_assign_users.html', 
                         project_id=project_id, 
                         all_users=all_users, 
                         assigned_user_ids=assigned_user_ids)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role']
        if db.get_user_by_username(username):
            flash('Username already exists. Please choose another.')
            return render_template('register.html')
        db.create_user(username, password, role)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        row = db.get_user_by_username(username)
        if row and db.verify_password(row[2], password):
            user = User(*row[:4])
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('fill_timesheet'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

def get_week_start_date(date_str=None):
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_obj = datetime.now().date()
    
    # Get Monday of the week
    days_since_monday = date_obj.weekday()
    monday = date_obj - timedelta(days=days_since_monday)
    return monday

@app.route('/timesheet', methods=['GET', 'POST'])
@login_required
def fill_timesheet():
    # Get view type (daily, weekly, monthly) - default to weekly
    view_type = request.args.get('view', 'weekly')
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if request.method == 'POST':
        # Handle multiple timesheet entries
        entries_data = request.form.getlist('entries')
        for entry_data in entries_data:
            if entry_data.strip():
                parts = entry_data.split('|')
                if len(parts) >= 5:
                    date, project_id, task_category_id, hours, description = parts[:5]
                    if hours and float(hours) > 0:
                        db.insert_timesheet_entry_enhanced(
                            current_user.id, date, project_id, task_category_id, hours, description
                        )
        
        flash('✅ Timesheet entries saved successfully!')
        return redirect(url_for('fill_timesheet', view=view_type, date=selected_date))
    
    # Get projects and task categories
    projects = db.get_projects_with_ids_for_user(current_user.id)
    task_categories = db.get_all_task_categories()
    
    if view_type == 'daily':
        # Single day view
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        existing_entries = db.get_timesheet_entries_for_day(current_user.id, date_obj)
        day_total = db.get_day_total_hours(current_user.id, date_obj)
        
        return render_template('timesheet_daily.html',
                             current_date=date_obj,
                             existing_entries=existing_entries,
                             projects=projects,
                             task_categories=task_categories,
                             day_total=day_total,
                             view_type=view_type,
                             user=current_user)
    
    elif view_type == 'monthly':
        # Monthly view
        year, month = map(int, selected_date.split('-')[:2])
        month_start = datetime(year, month, 1).date()
        month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        # Get all dates in the month
        month_dates = []
        current_date = month_start
        while current_date <= month_end:
            month_dates.append(current_date)
            current_date += timedelta(days=1)
        
        existing_entries = db.get_timesheet_entries_for_month(current_user.id, month_start, month_end)
        month_total = db.get_month_total_hours(current_user.id, month_start, month_end)
        
        return render_template('timesheet_monthly.html',
                             month_dates=month_dates,
                             month_start=month_start,
                             existing_entries=existing_entries,
                             projects=projects,
                             task_categories=task_categories,
                             month_total=month_total,
                             view_type=view_type,
                             user=current_user)
    
    else:  # weekly view
        week_start = get_week_start_date(selected_date)
        week_end = week_start + timedelta(days=6)
        week_dates = [week_start + timedelta(days=i) for i in range(7)]
        
        # Get existing entries for the week
        existing_entries = db.get_timesheet_entries_for_week(current_user.id, week_start)
        week_total = db.get_week_total_hours(current_user.id, week_start)
        
        return render_template('timesheet_weekly.html', 
                             week_dates=week_dates, 
                             week_start=week_start,
                             week_end=week_end,
                             existing_entries=existing_entries,
                             projects=projects,
                             task_categories=task_categories,
                             week_total=week_total,
                             view_type=view_type,
                             user=current_user,
                             timedelta=timedelta)

@app.route('/timesheet/submit-week', methods=['POST'])
@login_required
def submit_weekly_timesheet():
    week_start_str = request.form.get('week_start')
    if week_start_str:
        week_start = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        db.submit_weekly_timesheet(current_user.id, week_start)
        flash('✅ Weekly timesheet submitted successfully!')
    return redirect(url_for('fill_timesheet', view='weekly'))

@app.route('/timesheet/change-date', methods=['POST'])
@login_required
def change_date():
    direction = request.form.get('direction')
    current_date = request.form.get('current_date', datetime.now().strftime('%Y-%m-%d'))
    view_type = request.form.get('view_type', 'weekly')
    
    current_date_obj = datetime.strptime(current_date, '%Y-%m-%d').date()
    
    if view_type == 'daily':
        # Daily navigation: move by 1 day
        if direction == 'prev':
            new_date = current_date_obj - timedelta(days=1)
        else:  # next
            new_date = current_date_obj + timedelta(days=1)
        return redirect(url_for('fill_timesheet', view='daily', date=new_date.strftime('%Y-%m-%d')))
    
    elif view_type == 'weekly':
        # Weekly navigation: move by 7 days
        current_week_start = get_week_start_date(current_date)
        if direction == 'prev':
            new_week_start = current_week_start - timedelta(days=7)
        else:  # next
            new_week_start = current_week_start + timedelta(days=7)
        return redirect(url_for('fill_timesheet', view='weekly', date=new_week_start.strftime('%Y-%m-%d')))
    
    elif view_type == 'monthly':
        # Monthly navigation: move by 1 month
        year = current_date_obj.year
        month = current_date_obj.month
        
        if direction == 'prev':
            if month == 1:
                new_year = year - 1
                new_month = 12
            else:
                new_year = year
                new_month = month - 1
        else:  # next
            if month == 12:
                new_year = year + 1
                new_month = 1
            else:
                new_year = year
                new_month = month + 1
        
        new_date = datetime(new_year, new_month, 1).date()
        return redirect(url_for('fill_timesheet', view='monthly', date=new_date.strftime('%Y-%m-%d')))
    
    # Default fallback to weekly
    return redirect(url_for('fill_timesheet', view='weekly'))

@app.route('/timesheet/save-row', methods=['POST'])
@login_required
def save_row():
    try:
        project_id = request.form.get('project_id')
        task_id = request.form.get('task_id')
        description = request.form.get('description', '')
        hours_data = json.loads(request.form.get('hours_data', '[]'))
        
        if not project_id or not task_id:
            return jsonify({'success': False, 'message': 'Project and Task are required'})
        
        # Get week start date
        week_start = get_week_start_date()
        
        # Save entries for each day with hours
        for day_index, hours in enumerate(hours_data):
            if hours > 0:
                date = week_start + timedelta(days=day_index)
                db.insert_timesheet_entry_enhanced(
                    current_user.id, 
                    date.strftime('%Y-%m-%d'), 
                    project_id, 
                    task_id, 
                    hours, 
                    description
                )
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/timesheet/update-row', methods=['POST'])
@login_required
def update_row():
    try:
        entry_id = request.form.get('entry_id')
        project_id = request.form.get('project_id')
        task_id = request.form.get('task_id')
        description = request.form.get('description', '')
        hours_data = json.loads(request.form.get('hours_data', '[]'))
        
        if not entry_id or not project_id or not task_id:
            return jsonify({'success': False, 'message': 'Entry ID, Project and Task are required'})
        
        # Update the entry
        db.update_timesheet_entry(
            entry_id,
            current_user.id,
            project_id,
            task_id,
            description,
            hours_data
        )
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/timesheet/delete-row', methods=['POST'])
@login_required
def delete_row():
    try:
        data = request.get_json()
        entry_id = data.get('entry_id')
        
        if not entry_id:
            return jsonify({'success': False, 'message': 'Entry ID is required'})
        
        # Delete the entry
        db.delete_timesheet_entry(entry_id, current_user.id)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/timesheet/delete-entry', methods=['POST'])
@login_required
def delete_entry():
    try:
        data = request.get_json()
        entry_id = data.get('entry_id')
        
        if not entry_id:
            return jsonify({'success': False, 'message': 'Entry ID is required'})
        
        # Delete the entry
        db.delete_timesheet_entry(entry_id, current_user.id)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/timesheet/save-entry', methods=['POST'])
@login_required
def save_entry():
    try:
        data = request.get_json()
        date = data.get('date')
        project_id = data.get('project_id')
        task_id = data.get('task_id')
        hours = data.get('hours')
        description = data.get('description', '')
        entry_id = data.get('entry_id')
        
        if not all([date, project_id, task_id, hours, description]):
            return jsonify({'success': False, 'message': 'All required fields must be filled'})
        
        if entry_id and entry_id != '':
            # Update existing entry
            db.update_timesheet_entry(
                entry_id,
                current_user.id,
                project_id,
                task_id,
                description,
                float(hours)
            )
            message = 'Entry updated successfully'
        else:
            # Create new entry
            db.insert_timesheet_entry_enhanced(
                current_user.id,
                date,
                project_id,
                task_id,
                hours,
                description
            )
            message = 'Entry created successfully'
        
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        user_details = db.get_user_by_id(current_user.id)
        if not db.verify_password(user_details[2], current_password):  # user_details[2] is password_hash
            flash('❌ Current password is incorrect', 'error')
            return redirect(url_for('profile'))
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('❌ New passwords do not match', 'error')
            return redirect(url_for('profile'))
        
        # Check password length
        if len(new_password) < 6:
            flash('❌ New password must be at least 6 characters long', 'error')
            return redirect(url_for('profile'))
        
        # Check if new password is same as current
        if current_password == new_password:
            flash('❌ New password must be different from current password', 'error')
            return redirect(url_for('profile'))
        
        # Update password
        try:
            if db.update_user_password(current_user.id, new_password):
                flash('✅ Password updated successfully!', 'success')
            else:
                flash('❌ Error updating password', 'error')
        except Exception as e:
            flash('❌ Error updating password: ' + str(e), 'error')
        
        return redirect(url_for('profile'))
    
    # Get user details
    user_details = db.get_user_by_id(current_user.id)
    return render_template('profile.html', user=user_details)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = db.get_all_users()
    return render_template('admin_users.html', users=users)

@app.route('/admin/change-password/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_change_password(user_id):
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if new_password != confirm_password:
        flash('❌ Passwords do not match', 'error')
        return redirect(url_for('admin_users'))
    
    if db.update_user_password(user_id, new_password):
        flash('✅ Password updated successfully!', 'success')
    else:
        flash('❌ Error updating password', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Get filter parameters
    start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    user_id = request.args.get('user_id', '')
    project_id = request.args.get('project_id', '')
    
    # Get filter options
    users = db.get_all_users()
    projects = db.get_all_projects()
    
    # Get filtered entries
    raw_entries = db.get_filtered_entries(start_date, end_date, user_id, project_id)
    
    # Convert tuples to objects for template
    entries = []
    for entry in raw_entries:
        entry_obj = type('Entry', (), {
            'id': entry[0],
            'date': datetime.strptime(entry[1], '%Y-%m-%d').date() if isinstance(entry[1], str) else entry[1],
            'project_name': entry[2],
            'task_name': entry[3],
            'hours': entry[4],
            'description': entry[5],
            'username': entry[6] if len(entry) > 6 else 'N/A'
        })()
        entries.append(entry_obj)
    
    # Calculate totals
    total_hours = sum(entry.hours for entry in entries) if entries else 0
    total_entries = len(entries) if entries else 0
    total_users = len(users) if users else 0
    total_projects = len(projects) if projects else 0
    
    # Create stats object
    stats = {
        'total_entries': total_entries,
        'total_hours': total_hours,
        'total_users': total_users,
        'total_projects': total_projects
    }
    
    # Create filters object
    filters = {
        'start_date': start_date,
        'end_date': end_date,
        'user_id': user_id,
        'project_id': project_id
    }
    
    return render_template('admin_dashboard.html', 
                         entries=entries, 
                         users=users, 
                         projects=projects,
                         stats=stats,
                         filters=filters)

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    # Get filter parameters
    start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    project_id = request.args.get('project_id', '')
    
    # Get user's projects
    projects = db.get_projects_with_ids_for_user(current_user.id)
    
    # Get filtered entries for current user
    entries = db.get_user_filtered_entries(current_user.id, start_date, end_date, project_id)
    
    # Calculate totals
    total_hours = sum(entry[4] for entry in entries) if entries else 0
    total_entries = len(entries) if entries else 0
    active_projects = len(projects) if projects else 0
    avg_hours_per_day = total_hours / 30 if total_hours > 0 else 0  # Assuming 30 days
    
    # Create stats object
    stats = {
        'total_entries': total_entries,
        'total_hours': total_hours,
        'active_projects': active_projects,
        'avg_hours_per_day': avg_hours_per_day
    }
    
    # Create filters object
    filters = {
        'start_date': start_date,
        'end_date': end_date,
        'project_id': project_id
    }
    
    return render_template('user_dashboard.html', 
                         entries=entries, 
                         projects=projects,
                         stats=stats,
                         filters=filters)

@app.route('/export-entries')
@login_required
def export_entries():
    # Get filter parameters
    start_date = request.args.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    project_id = request.args.get('project_id', '')
    
    # Get entries based on user role
    if current_user.role == 'admin':
        user_id = request.args.get('user_id', '')
        entries = db.get_filtered_entries(start_date, end_date, user_id, project_id)
    else:
        entries = db.get_user_filtered_entries(current_user.id, start_date, end_date, project_id)
    
    # Create CSV response
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'User', 'Project', 'Task Category', 'Hours', 'Description'])
    
    for entry in entries:
        writer.writerow([
            entry[1],  # date
            entry[6] if len(entry) > 6 else 'N/A',  # username
            entry[2],  # project name
            entry[3],  # task category
            entry[4],  # hours
            entry[5] or ''  # description
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=timesheet_entries_{start_date}_to_{end_date}.csv'}
    )


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
