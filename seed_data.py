import os
from dotenv import load_dotenv
import subprocess
import logging
import urllib.parse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_seeding.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

def get_connection_string():
    """Create PostgreSQL connection string from environment variables."""
    try:
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASSWORD')

        # Format connection string for pg_restore
        conn_string = f"postgresql://{db_user}:{urllib.parse.quote_plus(db_pass)}@{db_host}:{db_port}/{db_name}"
        return conn_string
    except Exception as e:
        logging.error(f"Error creating connection string: {str(e)}")
        return None

def restore_database():
    """Restore database from dump file using pg_restore."""
    try:
        conn_string = get_connection_string()
        if not conn_string:
            return False

        # Construct pg_restore command
        command = [
            'pg_restore',
            '--no-owner',  # Skip object ownership
            '--clean',     # Clean (drop) database objects before recreating
            '--if-exists', # Add IF EXISTS to DROP commands
            '--no-privileges',  # Skip restoration of access privileges (grant/revoke)
            '--no-comments',    # Do not output commands to restore comments
            '-d', conn_string,  # Connection string
            'OnlineRetaildb.sql'  # Input file
        ]

        # Execute pg_restore
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            logging.info("Database restored successfully")
            return True
        else:
            logging.error(f"Error restoring database: {result.stderr}")
            return False

    except Exception as e:
        logging.error(f"Error in restore_database: {str(e)}")
        return False

def verify_restore():
    """Verify that the database was restored correctly."""
    try:
        import psycopg2

        # Create connection
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            sslmode='require'
        )

        # Create cursor
        cur = conn.cursor()

        # List of tables to verify
        tables = ['customer', 'product', 'sales', 'time']

        for table in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                count = cur.fetchone()[0]
                logging.info(f"Table {table} has {count} records")
            except Exception as e:
                logging.error(f"Error verifying table {table}: {str(e)}")

        cur.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error verifying restore: {str(e)}")

def main():
    """Main function to coordinate database restoration process."""
    try:
        logging.info("Starting database restoration process...")

        # Restore database
        if restore_database():
            # Verify restoration
            logging.info("Verifying database restoration...")
            verify_restore()
            logging.info("Database restoration process completed successfully")
        else:
            logging.error("Database restoration failed")

    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main() 