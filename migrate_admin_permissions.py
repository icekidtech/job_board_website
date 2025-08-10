"""
Database migration script to add admin permissions support
Run this script to update your existing database with new admin features
"""

import sqlite3
import os
import json
from pathlib import Path
from werkzeug.security import generate_password_hash

# Get database path
PROJECT_ROOT = Path(__file__).parent
DATABASE_PATH = PROJECT_ROOT / 'job_board.db'

def migrate_database():
    """Add permissions and created_by columns to users table"""
    
    if not DATABASE_PATH.exists():
        print("Database file not found. Please run the application first to create the database.")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        migrations_needed = []
        
        if 'permissions' not in columns:
            migrations_needed.append("ALTER TABLE user ADD COLUMN permissions TEXT DEFAULT '{}'")
            
        if 'created_by' not in columns:
            migrations_needed.append("ALTER TABLE user ADD COLUMN created_by INTEGER")
        
        # Run migrations
        if migrations_needed:
            print("Running database migrations...")
            
            for migration in migrations_needed:
                print(f"Executing: {migration}")
                cursor.execute(migration)
            
            # Create default admin if none exists
            cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count == 0:
                print("No admin users found. Creating default admin...")
                
                # Create default admin with all permissions
                default_permissions = {
                    'manage_users': True,
                    'manage_jobs': True,
                    'manage_applications': True,
                    'view_reports': True,
                    'system_settings': True
                }
                
                # Hash the default password
                password_hash = generate_password_hash('admin123')
                
                cursor.execute("""
                    INSERT INTO user (username, email, password, role, permissions, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """, (
                    'admin',
                    'admin@jobboard.com',
                    password_hash,
                    'admin',
                    json.dumps(default_permissions),
                    1
                ))
                
                print("✅ Default admin created:")
                print("   Username: admin")
                print("   Email: admin@jobboard.com")
                print("   Password: admin123")
                print("⚠️  IMPORTANT: Please log in and change the password immediately!")
            
            # Commit changes
            conn.commit()
            print("Database migration completed successfully!")
            
        else:
            print("Database is already up to date.")
        
        # Close connection
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == '__main__':
    print("Starting database migration for admin permissions...")
    success = migrate_database()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("You can now use the enhanced admin features.")
        print("\nNext steps:")
        print("1. Run the application: python run.py")
        print("2. Log in with admin credentials")
        print("3. Change the default password")
        print("4. Create additional admins as needed")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")