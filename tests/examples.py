import random
import psycopg2 

some_list = ['alpha','beta','gamma','delta']

def find_and_replace(some_list, find, replace):
    # Finds and replaces the items passed in
    # Raises ValueError when the item is not found
    some_list[some_list.index(find)] = replace

def get_random_item():
    return random.choice(some_list)

def gather_input(prompt):
    return input(prompt)

def get_data_from_file(filename):
    contents = ""
    with open(filename) as myfile:
        contents += myfile.readline()
    return contents

def get_user_id_1():
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname="mydb",
        user="username",
        password="password",
        host="127.0.0.1",
        port="5432"
    )

    # Create a cursor object
    cur = conn.cursor()

    try:
        # Execute SQL query to fetch user at row 1
        cur.execute("SELECT * FROM USERS WHERE ID=1")       
        # Fetch the user data
        user = cur.fetchone()        
        # Commit the transaction
        conn.commit()        
        return user
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error fetching user:", error)
        # Rollback the transaction in case of error
        conn.rollback()        
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
    