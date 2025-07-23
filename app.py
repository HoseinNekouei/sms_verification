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
    conn = sqlite.connect(config.DATABASE_FILE_PATH)
    cur = conn.cursor()

    # Read the original serial database Excel file
    try:
        df_serial = pd.read_excel(file_path, sheet_name=0)
        print("Original Serial Database:")
        print(df_serial.head(5))

        # Save the DataFrame to SQLite database
        df_serial.to_sql('serials',conn, if_exists= 'replace', index= False)
        cur.execute("SELECT COUNT(*) FROM serials")
        num_serial_records= cur.fetchone()[0]

    except FileNotFoundError as e:
        print(f'Could not find serial_database.xlsx: {e}')


    # Read the faulty serial database Excel file
    try:
        df_faulty = pd.read_excel(file_path, sheet_name=1)
        print("Faulty Serial Database:")
        print(df_faulty.head())

        # Save the DataFrame to SQLite database
        df_faulty.to_sql('faulty_serials', conn, if_exists= 'append', index= False)
        cur.execute("SELECT COUNT(*) FROM FAULTY_SERIALS")
        num_faulty_serials= cur.fetchone()[0]

    except FileNotFoundError as e:
        print(f'Could not find faulty_serial_database.xlsx: {e}')

    # return number of row inserting
    return num_serial_records, num_faulty_serials
     
    # close the connection
    conn.close()


def check_serial():
    # Logic to check serial number
    return "Serial number checked"


if __name__ == '__main__':
    # check_serial()    
    app.run('127.0.0.1',5000,debug=True)
