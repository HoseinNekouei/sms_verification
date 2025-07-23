from flask import Flask, jsonify, request
import requests
import config
import pandas as pd
import sqlite3 as sqlite

app= Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the SMS Verification Service"


@app.route('/v1/process', methods=['POST'])
def process():
    
   response= request.get_json()
   message= response["message"]
   print(message)
   
   return jsonify(response),200  


def send_sms(number :str ,message :str):
    data= {'user':config.user_name,
           'pass': config.password,
           'line': config.line,
           'mobile': number,
           'message': message}

#    data= {'sender': config.sender,
#        'receptor': number, 
#        'message':message}
    print(data)
    response= requests.post(config.url, data=data)

    print(f'response is: {response}')


def import_database_from_excel(file_path):
    # Read the original serial database Excel file
    try:
        df_serial = pd.read_excel(file_path, sheet_name=0)
        print("Original Serial Database:")
        print(df_serial.head())

        # Connect to the SQLite database
        conn= sqlite.connect(config.DATABASE_FILE_PATH)
        cursor = conn.cursor()

        # drop the seials table if it exists
        cursor.execute('DROP TABLE IF EXISTS serials')

        # Create the serials table if it doesn't exist
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS serials (
                            id INTEGER primary key autoincrement,
                            ref TEXT NOT NULL,
                            start_serial TEXT NOT NULL,
                            end_serial TEXT NOT NULL,
                            date DATE NOT NULL,
                            serial_description TEXT NOT NULL
                        );
                    """)
    except FileNotFoundError as e:
        print(f'Could not find serial_database.xlsx: {e}')


    # Read the faulty serial database Excel file
    try:
        df_faulty = pd.read_excel(file_path, sheet_name=1)
        print("Faulty Serial Database:")
        print(df_faulty.head())

        # drop faulty table if it exists
        cursor.execute('DROP TABLE IF EXISTS faulty_serials')

        # Create the Faulty table if it doesn't exist
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS faulty_serials (
                            faulty TEXT NOT NULL
                        );
                    """)       
    except FileNotFoundError as e:
        print(f'Could not find faulty_serial_database.xlsx: {e}')


def check_serial():
    # Logic to check serial number
    return "Serial number checked"


if __name__ == '__main__':
    # check_serial()    
    import_database_from_excel(file_path=r'data/serial_database.xlsx')
    app.run('127.0.0.1',5000,debug=True)
