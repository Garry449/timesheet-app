# Nalashaa Timesheet Management System

A comprehensive web-based timesheet application for internal employees with role-based access control, project management, and professional UI.

## Features

- **User Authentication**: Login/logout with role-based access (Employee, Admin)
- **Project Management**: Admin can create projects and assign users
- **Timesheet Entry**: Daily, Weekly, and Monthly views with auto-calculation
- **Professional UI**: Responsive design with Nalashaa branding
- **Database Integration**: SQL Server with Windows Authentication

## Project Structure

```
timesheet_filler/
├── main.py                 # Flask application and routes
├── db.py                   # Database operations and queries
├── requirements.txt        # Python dependencies
├── create_admin.py         # Script to create admin user
├── templates/              # HTML templates
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── timesheet_weekly.html  # Weekly timesheet view
│   ├── timesheet_daily.html   # Daily timesheet view
│   ├── timesheet_monthly.html # Monthly timesheet view
│   ├── admin_projects.html    # Admin project creation
│   ├── admin_project_list.html # Admin project list
│   └── admin_assign_users.html # Admin user assignment
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   │   ├── timesheet.css      # General styles
│   │   └── timesheet-views.css # Timesheet view styles
│   ├── js/                # JavaScript files
│   │   └── timesheet.js       # Timesheet functionality
│   └── images/            # Image assets
│       └── nalashaa-logo.png  # Company logo
└── README.md              # This file
```

## Centralized CSS and JS Management

### CSS Files
- **`static/css/timesheet.css`**: General application styles (login, admin pages)
- **`static/css/timesheet-views.css`**: All timesheet view styles (daily, weekly, monthly)

### JavaScript Files
- **`static/js/timesheet.js`**: All timesheet functionality including:
  - Auto-calculation of total hours
  - Add/remove rows
  - Form submission handling
  - UI enhancements and keyboard shortcuts

### Benefits of Centralized Structure
- **Easy Maintenance**: All styles and scripts in one place
- **Consistent Design**: Shared styles across all views
- **Better Performance**: Reduced code duplication
- **Easier Debugging**: Clear separation of concerns

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   - Create SQL Server database named `timesheet`
   - Run the database creation scripts in `db.py`

3. **Create Admin User**:
   ```bash
   python create_admin.py
   ```

4. **Run Application**:
   ```bash
   python main.py
   ```

## Usage

### Admin Access
- Username: `admin`
- Password: `admin`
- Access: Project creation, user assignment, admin pages

### Employee Access
- Register new account
- Login with credentials
- Access timesheet entry pages

## Database Schema

### Tables
- `users`: User accounts and authentication
- `projects`: Project information
- `assignments`: User-project assignments
- `task_categories`: Task category definitions
- `timesheet_entries`: Timesheet data

## Development

### Adding New Features
1. **CSS**: Add styles to appropriate CSS file in `static/css/`
2. **JavaScript**: Add functionality to `static/js/timesheet.js`
3. **Templates**: Create new HTML files in `templates/`
4. **Routes**: Add Flask routes in `main.py`
5. **Database**: Add functions in `db.py`

### Styling Guidelines
- Use professional color scheme (blues, grays, whites)
- Maintain responsive design for all screen sizes
- Follow Nalashaa branding guidelines
- Ensure accessibility compliance

### JavaScript Guidelines
- Use centralized `timesheet.js` for all functionality
- Implement proper error handling
- Add keyboard shortcuts for better UX
- Ensure cross-browser compatibility

## Troubleshooting

### Common Issues
1. **Database Connection**: Ensure SQL Server is running and Windows Authentication is enabled
2. **CSS Not Loading**: Check file paths in templates
3. **JavaScript Errors**: Verify `timesheet.js` is properly loaded
4. **Responsive Issues**: Test on different screen sizes

### Debug Mode
Enable Flask debug mode for development:
```python
app.run(debug=True)
```

## Future Enhancements

- Timesheet approval workflow
- Email notifications and reminders
- Advanced reporting and analytics
- Export functionality (Excel/PDF)
- Mobile app integration

## Support

For technical support, contact: info@nalashaa.com

