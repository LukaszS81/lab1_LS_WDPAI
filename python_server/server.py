import json
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
import psycopg2
import os
import time

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError as e:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            print(e)
            time.sleep(5)

conn = connect_to_db()
cursor = conn.cursor()
def fetch_users():
    cursor.execute("SELECT id, first_name, last_name, role FROM users")
    users = cursor.fetchall()
    return [{"id": user[0], "first_name": user[1], "last_name": user[2], "role": user[3]} for user in users]



# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):

    user_list = [
        {
            'id': 1,
            'first_name': 'Michal',
            'last_name': 'Mucha',
            'role': 'Instructor'
        }
    ]

    def do_OPTIONS(self):

        self.send_response(200, "OK")

        self.send_header("Access-Control-Allow-Origin", "*")

        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()
# Handles GET requests, responds with the list of users in JSON format.
    def do_GET(self) -> None:
        try:
            cursor.execute("SELECT id, first_name, last_name, role FROM users;")
            users = cursor.fetchall()  # Fetch all rows from the users table
            self.user_list = [
                {
                    'id': user[0],
                    'first_name': user[1],
                    'last_name': user[2],
                    'role': user[3]
                }
                for user in users
            ]

            self.wfile.write(json.dumps(self.user_list).encode())  # Sends user list as JSON response.

        except Exception as e:
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        first_name = received_data.get('firstName')
        last_name = received_data.get('lastName')
        role = received_data.get('role')

        cursor.execute(
            "INSERT INTO users (first_name, last_name, role) VALUES (%s, %s, %s)",
            (first_name, last_name, role)
        )
        conn.commit()

        user_list = fetch_users()

        self.wfile.write(json.dumps(user_list).encode())

    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])

        post_data: bytes = self.rfile.read(content_length)

        received_data: dict = json.loads(post_data.decode())

        user_id = received_data['id']

        # SimpleRequestHandler.user_list = [user for user in self.user_list if user['id'] != user_id]

        cursor.execute(
            "DELETE FROM users WHERE id = %s", (user_id,)
            )
        conn.commit()

        user_list = fetch_users()

        self.wfile.write(json.dumps(user_list).encode())

def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    server_address: tuple = ('', port)

    httpd: HTTPServer = server_class(server_address, handler_class)

    print(f"Starting HTTP server on port {port}...")

    httpd.serve_forever()

if __name__ == '__main__':
    run()