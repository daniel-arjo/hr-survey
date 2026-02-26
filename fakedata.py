import psycopg2
from faker import Faker
import random
from datetime import timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
fake = Faker('pt-BR')

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


def insert_data():
    connection = None
    cursor = None
    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        print("Connection successful!")
        
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        
        # inserting users
        ar_list = set()
        print("Generating Users")
        for _ in range(250):
            name = fake.name()
            email = fake.unique.email()
            address = fake.address()
            phone_number = fake.unique.phone_number()
            user_type = random.choice(['student', 'student', 'student', 'admin'])
            ar = str(random.randint(100000, 999999))
            while(ar in ar_list):
                ar = str(random.randint(100000, 999999))
            ar_list.add(ar)
            query_users = "insert into users (name, email, address, phone_number, ar, user_type) values (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query_users, (name, email, address, phone_number, ar, user_type))

        # inserting books
        print("Generating Books")
        for _ in range(3000):
            title = fake.catch_phrase()
            author = fake.name()
            isbn = fake.isbn13()
            status = random.choice(['available', 'available', 'loaned'])

            query_books = "insert into books (title, author, isbn, status) values (%s, %s, %s, %s)"
            cursor.execute(query_books, (title, author, isbn, status))

        print("Generating Loans")
        # inserting loans
        cursor.execute("select id from users;")
        users_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("select id from books where status = 'loaned';")
        loaned_books_ids = [row[0] for row in cursor.fetchall()]

        for book_id in loaned_books_ids:
            user_id = random.choice(users_ids)
            loan_date = fake.date_between(start_date='-30d', end_date='today')
            return_date = loan_date + timedelta(days=14)

            query_loans = "insert into loans (user_id, book_id, loan_date, return_date, status) values (%s, %s, %s, %s, %s)"
            cursor.execute(query_loans, (user_id, book_id, loan_date, return_date, 'active'))
        
        connection.commit()
        print("Data Generation Success!")

    except Exception as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
        
    finally:
        # Close the cursor and connection
        if cursor: cursor.close()
        if connection: connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    insert_data()
   
        



