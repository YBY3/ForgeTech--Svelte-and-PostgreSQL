import os
import psycopg2

# THIS WILL RESET THE DATABASE

conn = psycopg2.connect(
        host="161.35.106.21",
        port="5432",
        database="project_55_db",
        user=os.environ['project_55_user'],
        password=os.environ['project_55_password'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Create team_images table
cur.execute('DROP TABLE IF EXISTS team_images;')
cur.execute('CREATE TABLE team_images ('
            'id serial PRIMARY KEY,'
            'image_owner varchar(80) NOT NULL,'
            'image_name varchar(80) UNIQUE NOT NULL,'
            'image_path varchar(255) NOT NULL'
            ');')

# Commit change
conn.commit()

cur.close()
conn.close()