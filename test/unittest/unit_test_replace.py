import unittest, replace, json
from typing import Any, List, Dict, Optional, NoReturn
import library as lib

log_params = {
  'folder' : 'test/log',
  'base_file_name' : 'pyapp.log',
  'level':lib.logging.DEBUG,
  'format':'%(asctime)s:%(levelname)s:%(message)s',
  'encoding':'utf-8',
  'full_path_name':'',
  'clean':{'remove':True, 'days':0,'seconds':0, 'quantity':1}
}

logger = lib.configure_logging(log_params)

class Test_Replace(unittest.TestCase):
  def setUp(self) -> None:
    self.test_data_file = 'test/files/test_replace_data.json'
    self.test_input_file = 'test/files/test_input.txt'
    self.test_output_file = 'test/files/test_output.txt'
  
  def load_json(self, file_name:str) -> Dict:
    with open(file_name, 'r') as file:
      return json.load(file)

  def load_text(self, file_name:str) -> str:
    with open(file_name, 'r') as file:
      return file.read()

  def test_load_data_file(self):
    data = self.load_json(self.test_data_file)
    self.assertEqual(data['ABN'], 'ABN Amro')
    self.assertEqual(data['ING'], 'ING Bank')
  
  def test_several_replacements(self):  
    self .assertEqual(replace.event_handler(replace.replace_function, logger=logger, text='ABN')['result'], 'ABN Amro')
    self .assertEqual(replace.event_handler(replace.replace_function, logger=logger, text='aBn')['result'], 'ABN Amro')
    self .assertEqual(replace.event_handler(replace.replace_function, logger=logger, text='abn.')['result'], 'ABN Amro.')
    self .assertEqual(replace.event_handler(replace.replace_function, logger=logger, text='/abn')['result'], '/ABN Amro')

  def test_reverse_replacement(self):
    self .assertEqual(replace.event_handler(replace.replace_function, logger=logger, text='abn amro')['result'], 'ABN Amro')

  def test_neglect_inwords(self):
    self .assertEqual(replace.event_handler(replace.replace_function, logger=logger, text='ABNORMAL')['result'], 'ABNORMAL')

  def test_event_handler(self):
    test_input_string = self.load_text(self.test_input_file)
    test_output_string = self.load_text(self.test_output_file)
    result = replace.event_handler(replace.replace_function, logger=logger, text=test_input_string)
    self.assertEqual(result['result'], test_output_string)

if __name__ == '__main__':
  unittest.main()

