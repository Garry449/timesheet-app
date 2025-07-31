#!/usr/bin/env python3
"""
Setup script for cloud PostgreSQL database
Run this once after setting up your PostgreSQL database
"""

import os
import pg8000

def setup_database():
    """Create tables and insert initial data for cloud deployment"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("DATABASE_URL not found in environment variables - skipping database setup")
        print("Please set DATABASE_URL environment variable to connect to PostgreSQL")
        return True  # Return True to not fail the build
    
    conn = None
    try:
        # Connect to database
        conn = pg8000.connect(database_url)
        cursor = conn.cursor()
        
        # Create tables
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
        
        # Insert default admin user if not exists
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            from werkzeug.security import generate_password_hash
            admin_password = generate_password_hash('admin123')
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ('admin', admin_password, 'admin')
            )
            print("Created admin user with password: admin123")
        
        # Insert default task categories if not exists
        default_categories = [
            'Development',
            'Testing',
            'Documentation',
            'Meeting',
            'Planning',
            'Code Review',
            'Bug Fix',
            'Research',
            'Training'
        ]
        
        for category in default_categories:
            cursor.execute("SELECT id FROM task_categories WHERE name = %s", (category,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO task_categories (name) VALUES (%s)", (category,))
        
        # Insert default project if not exists
        cursor.execute("SELECT id FROM projects WHERE name = 'Default Project'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO projects (name, start_date, end_date) VALUES (%s, %s, %s)",
                ('Default Project', '2024-01-01', '2025-12-31')
            )
            project_id = cursor.fetchone()[0]
            
            # Assign admin to default project
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            admin_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO user_projects (user_id, project_id) VALUES (%s, %s)",
                (admin_id, project_id)
            )
        
        conn.commit()
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database() 