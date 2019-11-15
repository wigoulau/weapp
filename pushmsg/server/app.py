from flask import Flask, request
import pushmsg
import json

app = Flask(__name__)

@app.route('/notification', methods=['POST'])
def notification():
    print('notification')
    #print(request.headers)
    data = request.get_json()
    #print(type(data))
    #print(data)
    #print(data['openid'])
    #print(data['form_id'])
    res = pushmsg.notifications(data['openid'], data['form_id'])

    return res

if __name__ == '__main__':
    app.debug = True
    app.run('192.168.188.163', port=4000, threaded=True)
