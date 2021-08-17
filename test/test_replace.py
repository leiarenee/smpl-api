import unittest, replace, json
from typing import Any, List, Dict, Optional, NoReturn

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
    self .assertEqual(replace.event_handler(replace.replace_function, text='ABN')['result'], 'ABN Amro')
    self .assertEqual(replace.event_handler(replace.replace_function, text='aBn')['result'], 'ABN Amro')
    self .assertEqual(replace.event_handler(replace.replace_function, text='abn.')['result'], 'ABN Amro.')
    self .assertEqual(replace.event_handler(replace.replace_function, text='/abn')['result'], '/ABN Amro')

  def test_reverse_replacement(self):
    self .assertEqual(replace.event_handler(replace.replace_function, text='abn amro')['result'], 'ABN Amro')

  def test_neglect_inwords(self):
    self .assertEqual(replace.event_handler(replace.replace_function, text='ABNORMAL')['result'], 'ABNORMAL')

  def test_event_handler(self):
    test_input_string = self.load_text(self.test_input_file)
    test_output_string = self.load_text(self.test_output_file)
    result = replace.event_handler(replace.replace_function, text=test_input_string)
    self.assertEqual(result['result'], test_output_string)

if __name__ == '__main__':
  unittest.main()

