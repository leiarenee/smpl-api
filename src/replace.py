
from typing import Dict, Any, List, Optional, NoReturn
import library as lib
import json, re

# Global Variables
debug_mode = True
interactive = False
replace_data_file = 'replace_data.json'
logger = None

# Default log parameters
log_params = {
  'folder' : 'logs',
  'base_file_name' : 'pyapp.log',
  'level':lib.logging.DEBUG,
  'format':'%(asctime)s:%(levelname)s:%(message)s',
  'encoding':'utf-8',
  'full_path_name':'',
  'clean':{'remove':True, 'days':0,'seconds':0, 'quantity':10}
}

#@lib.safe_run(log_params=log_params, debug_mode=debug_mode)
def regexp_replace(search, replace, text):
  result = text
  pattern = '(^|[^\\\p{L}])('
  # sample r'(^|[^\p{L}])([Aa][Bb][Nn])([^\p{L}]|$)'
  for char in search:
    pattern = pattern + f'[{char.upper()}{char.lower()}]'
  pattern += ')([^\\\p{L}]|$)'
  result = re.sub(pattern, r'\1' + f'{replace}' + r'\3' , result)
  return result

#@lib.safe_run(log_params=log_params, debug_mode=debug_mode)
def replace_function(text:str) -> Dict: 
  """Replaces given keyword with the corresponding value within the database

  Args:
      keyword (str): Text to be replaced.

  Returns:
      Dict: Replaced value in following format. {'result':'[Replacement]'}
  """

  try:
    with open(file=replace_data_file, mode='r') as file:
      json_data = json.load(file)
    result = text
    for search, replace in json_data.items():
      # Inverse replace to avoid multiple replacements if replace string contains search string
      result = regexp_replace(replace, search, result)
      # Real replacement of serch string with replacement
      result = regexp_replace(search, replace, result)
      pass
  # Check if data file exists
  except OSError as err:
    if err.errno == 2 and not debug_mode:
      lib.error_handling(f'Data file "{replace_data_file}" file does not exist')
    else:raise
  else:
    return { 'result' : result}

def event_handler(fnc, *args, **kwargs) -> Any:
  """Initializes environment and calls the function with parameters
  Args:
    fnc (Function): Function to called.
    args (Tuple): Positionsl arguments.
    kwargs (Dict): Keyword arguments
  
  Keyworg Args:
    **kwargs (): Dicti
  Returns:
      result (Any): Result of function
  """
  global logger
  # Initialize logging
  if not log_params['full_path_name']:
    logger = lib.configure_logging(log_params)
  logger.debug('Module Started.')
  result = lib.safe_run(fnc, log_params=log_params, debug_mode=debug_mode)(*args, **kwargs)
  logger.debug('End of Main Routine.')
  return result

# Main routine to test the program in command line
if __name__ == '__main__':
  debug_mode = False
  keyword = ''
  interactive = True
  
  while keyword != 'q':
    keyword = input('Please Enter Keywod (q for exit) : ')
    if keyword != 'q':
      result = event_handler(replace_function, keyword)
      if 'result' in result:
        print(result)
    else:
      print('Exiting with "q" command.')
      
 