import pyodbc

def create_connection(server_name, database_name, username, password):
    connection = None
    try:
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
        )
        print("Connection to SQL Server DB successful")
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def fetch_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")
    return result    

# Update these variables with your SQL Server configuration
server_name = "localhost\\SQLEXPRESS"
database_name = "SAPM"
username = "webauth2"
password = "Admin@12345"

connection = create_connection(server_name, database_name, username, password)
select_query = "SELECT * FROM JetFormat"
rows = fetch_query(connection, select_query)

# Display the fetched data
for row in rows:
    print(row)