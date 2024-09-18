from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from datetime import datetime

app = Flask(__name__)

# Database connection parameters
server = 'localhost\\SQLEXPRESS'
database = 'PrinterDatabase'
username = 'webauth2'
password = 'Admin@12345'
driver = '{ODBC Driver 17 for SQL Server}'

# Function to get transactions for a specific date
def get_transactions(date):
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()
        query = """
            SELECT
                [S.No],  -- Corrected column name
                [DateAndTime],  -- Corrected column name
                [Shift],
                [ProductId],
                [GSM],
                [BF],
                [Reel_Id],
                [Reel_Size (cm)],
                [Reel_Dia (cm)],
                [Weight (Kg)]  -- Corrected column name
            FROM PrinterData
            WHERE CAST([DateAndTime] AS DATE) = ?
        """
        cursor.execute(query, date)
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Debugging: Print the fetched transactions
        print("Fetched transactions:", transactions)
        
        return transactions
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return []

# Function to add a new transaction
def add_transaction(shift, product_id, gsm, bf, reel_id, reel_size, reel_dia, weight):
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()
        query = """
            INSERT INTO PrinterData (
                [DateAndTime],
                [Shift],
                [ProductId],
                [GSM],
                [BF],
                [Reel_Id],
                [Reel_Size (cm)],
                [Reel_Dia (cm)],
                [Weight (Kg)]
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        current_datetime = datetime.now()
        cursor.execute(query, (
            current_datetime,
            shift,
            product_id,
            gsm,
            bf,
            reel_id,
            reel_size,
            reel_dia,
            weight
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return False

@app.route('/', methods=['GET'])
def index():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    print("Requested date:", date_str)  # Debugging: Print the requested date
    transactions = get_transactions(date_str)
    return render_template('index.html', transactions=transactions, date=date_str)

@app.route('/enter-data', methods=['GET', 'POST'])
def enter_data():
    if request.method == 'POST':
        shift = request.form['shift']
        product_id = request.form['product_id']
        gsm = request.form['gsm']
        bf = request.form['bf']
        reel_id = request.form['reel_id']
        reel_size = request.form['reel_size']
        reel_dia = request.form['reel_dia']
        weight = request.form['weight']
        
        # Add the transaction to the database
        success = add_transaction(shift, product_id, gsm, bf, reel_id, reel_size, reel_dia, weight)
        
        if success:
            return redirect(url_for('enter_data'))
        else:
            return "There was an error adding the transaction to the database."

    return render_template('enter_data.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
