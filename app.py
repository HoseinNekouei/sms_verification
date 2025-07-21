from flask import Flask, jsonify, request

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

def send_sms(number, message):
    # Logic to send SMS
    return "SMS sent"

def check_serial():
    # Logic to check serial number
    return "Serial number checked"

if __name__ == '__main__':
    app.run('127.0.0.1',5000,debug=True)
