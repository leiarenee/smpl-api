import json
import pdb
import logging
import collections
import time
import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import replace

def handleError(err):
    logging.error(err)
    return jsonify({'error':str(err)})

app = Flask(__name__)
log = logging.getLogger('werkzeug')
auth = HTTPBasicAuth()

#Provides support for sending cross origin headers
CORS(app)

#Normally, is stored encrypted in database
userStore = {
    "replace": "replace" # cmVwbGFjZTpyZXBsYWNl
}

#Verify username and password
@auth.verify_password
def verifyUser(username, password):
    if not (username and password):
        return False
    return userStore.get(username) == password

#replace api function
@app.route('/api/replace', methods=['POST', 'GET'])
@auth.login_required
def replaceapi():
  
  reqArgs = request.args.getlist("key")
  data = json.loads(request.data)
  
  result = replace.event_handler(replace.replace_function, data['text'])
  print(result)
  #pdb.set_trace()
  return jsonify(result)
  

if __name__ == '__main__':
  os.environ['FLASK_ENV']='development'
  app.run(host='localhost', port=2000, debug=True)
