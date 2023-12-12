from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import sqlite3


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            email = params.get('email', [''])[0]
            password = params.get('password', [''])[0]
            age = params.get('age', [''])[0]
            gender = params.get('gender', [''])[0]

            # Підключення до бази даних
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()

            # Створення таблиці користувачів, якщо вона не існує
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT
                )
            ''')
            conn.commit()

            # Реєстрація нового користувача
            cursor.execute('''
                INSERT INTO users (email, password, age, gender)
                VALUES (?, ?, ?, ?)
            ''', (email, password, age, gender))
            conn.commit()

            # Закриття підключення до бази даних
            conn.close()

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print('Server started on http://localhost:8000/')
    httpd.serve_forever()
