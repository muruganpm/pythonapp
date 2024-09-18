from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

def create_connection():
    server_name = "localhost\\SQLEXPRESS"
    database_name = "PrinterDatabase"
    username = "webauth2"
    password = "Admin@12345"
    
    connection = None
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
        )
        print("Connection to SQL Server DB successful")
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def fetch_data():
    connection = create_connection()
    if connection:
        query = "SELECT * FROM PrinterData WHERE CONVERT(date, DateAndTime) = CONVERT(date, GETDATE())"
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        connection.close()
        return rows
    else:
        return []

@app.route('/')
def index():
    data = fetch_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host = '0.0.0.0' , debug=True, port=5000)
