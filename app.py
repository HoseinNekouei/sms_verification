from flask import Flask, jsonify, request
import requests
import config

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


def check_serial():
    # Logic to check serial number
    return "Serial number checked"

if __name__ == '__main__':
    send_sms('09155603281','this message send via payamkotah service')
    app.run('127.0.0.1',5000,debug=True)
