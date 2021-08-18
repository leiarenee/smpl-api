import pytest
from flaskapi import create_app
import pdb

headers = {'Content-Type': 'application/json','Authorization': 'Basic cmVwbGFjZTpyZXBsYWNl'}
test_input_file = 'test/files/test_input.txt'
test_output_file = 'test/files/test_output.txt'


@pytest.fixture
def client():
  app = create_app({'TESTING': True})
  with app.test_client() as client:
    with app.app_context():
        pass
    yield client

def load_text(file_name:str) -> str:
  with open(file_name, 'r') as file:
    return file.read()

def test_api_route(client):
  result = client.post('/api/replace', data={} , follow_redirects=True)
  assert b'Unauthorized Access' in result.data
  
def test_authorization(client):
  body = '{"text" : "sample_text_for_check"}'
  result = client.post('/api/replace', follow_redirects=True, data=body, headers=headers)
  assert b'sample_text_for_check' in result.data
  
def test_replacement(client):
  test_input_string = load_text(test_input_file)
  test_output_string = load_text(test_output_file)
  body = '{"text" : "' + test_input_string + '"}'
  result = client.post('/api/replace', follow_redirects=True, data=body, headers=headers)
  assert test_output_string.encode('utf-8') in result.data

def test_key_error(client):
  body = '{"ext" : "Sample"}'
  result = client.post('/api/replace', follow_redirects=True, data=body, headers=headers)
  assert b'Text field must be specified' in result.data

def test_json_error(client):
  body = '{"ext" : Sample}'
  result = client.post('/api/replace', follow_redirects=True, data=body, headers=headers)
  assert b'JSONDecodeError' in result.data