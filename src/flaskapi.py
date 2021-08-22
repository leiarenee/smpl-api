import json
from json.decoder import JSONDecodeError
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
import library as lib
from http import HTTPStatus
import dotenv
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Default log parameters
log_params = {
  'folder' : 'log',
  'base_file_name' : 'pyapp.log',
  'level':lib.logging.DEBUG,
  'format':'%(asctime)s:%(levelname)s:%(message)s',
  'encoding':'utf-8',
  'full_path_name':'',
  'clean':{'remove':True, 'days':0,'seconds':0, 'quantity':1}
}
#logger = lib.configure_logging(log_params)
logger = logging.getLogger()
def handleError(err,return_code=500):
  http_status = HTTPStatus(return_code).phrase
  error_message = repr(err).replace("'",'')
  logger.error(f'Server HTTP {return_code} {http_status} : "{error_message}"')
  return jsonify({'error':repr(err).replace("'",'')}), return_code

def create_app(test_config=None):
  """Create and configure an instance of the Flask application."""
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY="dev"
  )

  if test_config is None:
      # load the instance config, if it exists, when not testing
      app.config.from_pyfile("config.py", silent=True)
  else:
      # load the test config if passed in
      app.config.update(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  
  #logger = logging.getLogger('werkzeug')
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
  @lib.safe_run
  def replaceapi():  
    try:
      data = json.loads(request.data)
      result = replace.event_handler(replace.replace_function,logger, data['text'])
      #print(result)
      #pdb.set_trace()
    except KeyError as err:
      return handleError(f'Text field must be specified', 400)  
      #pdb.set_trace()
    except JSONDecodeError as err:
      return handleError(err, 400)
    except Exception as err:
      return handleError(err, 500)
    else:
      logger.info(f'Server HTTP 200 {HTTPStatus(200).phrase} : {result}')
      return jsonify(result)
      
  return app


if __name__ == '__main__':
  env_file = '.env'
  HOST = dotenv.get_key(env_file, 'HOST')
  PORT = dotenv.get_key(env_file, 'PORT')
  FLASK_DEBUG = dotenv.get_key(env_file, 'FLASK_DEBUG')
  XRAY = dotenv.get_key(env_file,'XRAY')
  app = create_app()
  if XRAY.lower == 'true':
    xray_recorder.configure(service='Flask-API')
    XRayMiddleware(app, xray_recorder)
  print (f'Server listens on {HOST}:{PORT}')
  app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
