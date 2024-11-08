import json
import random
from utils import random_int
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
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)

conn = connect_to_db()
cursor = conn.cursor()



# Define the request handler class by extending BaseHTTPRequestHandler.
# This class will handle HTTP requests that the server receives.
class SimpleRequestHandler(BaseHTTPRequestHandler):

    user_list = [
            {
                'id': 1,
                'first_name': 'Jan',
                'last_name': 'Kowalski',
                'role': 'IT Specialist'
            },
            {
                'id': 2,
                'first_name': 'Andrew',
                'last_name': 'Lewis',
                'role': 'Student'
            },
            {
                'id': 3,
                'first_name': 'Stephens',
                'last_name': 'Huff',
                'role': 'HR'
            }
        ]

    def do_OPTIONS(self):

        self.send_response(200, "OK")

        self.send_header("Access-Control-Allow-Origin", "*")

        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)

        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        self.wfile.write(json.dumps(self.user_list).encode()) # WARNING: user_list hardcoded

    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])

        post_data: bytes = self.rfile.read(content_length)

        received_data: dict = json.loads(post_data.decode())

        newUser = {
            'id': random_int(),
            'first_name': received_data['firstName'],
            'last_name': received_data['lastName'],
            'role': received_data['role']
        }

        self.user_list.append(newUser)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        self.wfile.write(json.dumps(self.user_list).encode())

    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])

        post_data: bytes = self.rfile.read(content_length)

        received_data: dict = json.loads(post_data.decode())

        user_id = received_data['id']

        SimpleRequestHandler.user_list = [user for user in self.user_list if user['id'] != user_id]

        self.send_response(200)
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        self.wfile.write(json.dumps(self.user_list).encode())



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