@app.route('/setup-database')
def setup_database_route():
    """Route to set up database tables"""
    try:
        import db_simple as db
        
        # Create tables
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Create tables SQL
        create_tables_sql = """
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Projects table
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            start_date DATE,
            end_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- User projects relationship
        CREATE TABLE IF NOT EXISTS user_projects (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
            UNIQUE(user_id, project_id)
        );
        
        -- Task categories table
        CREATE TABLE IF NOT EXISTS task_categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Timesheet entries table
        CREATE TABLE IF NOT EXISTS timesheet_entries (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
            task_category_id INTEGER REFERENCES task_categories(id) ON DELETE CASCADE,
            hours DECIMAL(4,2) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_tables_sql)
        
        # Insert default admin user
        from werkzeug.security import generate_password_hash
        admin_password = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) ON CONFLICT (username) DO NOTHING",
            ('admin', admin_password, 'admin')
        )
        
        # Insert default task categories
        default_categories = [
            'Development', 'Testing', 'Documentation', 'Meeting', 
            'Planning', 'Code Review', 'Bug Fix', 'Research', 'Training'
        ]
        
        for category in default_categories:
            cursor.execute("INSERT INTO task_categories (name) VALUES (%s) ON CONFLICT DO NOTHING", (category,))
        
        # Insert default project
        cursor.execute(
            "INSERT INTO projects (name, start_date, end_date) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            ('Default Project', '2024-01-01', '2025-12-31')
        )
        
        conn.commit()
        conn.close()
        
        return "Database setup completed successfully! You can now login with admin/admin123"
        
    except Exception as e:
        return f"Error setting up database: {str(e)}" 