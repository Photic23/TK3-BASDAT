import psycopg2
import os

def get_db_connection():
    try:
        # Get database credentials from environment variables
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
        db_host = os.environ.get("DB_HOST")
        db_port = os.environ.get("DB_PORT")

        # Establish a connection to the database
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        # Print "Berhasil" if connection is successful
        print("Berhasil")

        # Create a cursor object
        cursor = connection.cursor()

        # Execute SQL commands to set the search path and list tables in the schema
        cursor.execute("SET SEARCH_PATH TO MARMUT")

        return connection

    except psycopg2.Error as e:
        print("Error:", e)


