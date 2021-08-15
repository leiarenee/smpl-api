
from typing import Dict
import library as lib
import json

# Global Variables
debug_mode = False
interactive = False
replace_data_file = 'replace_data.json'

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

@lib.safe_run(log_params=log_params)
def replace_function(keyword:str) -> Dict: 
  """Replaces given keyword with the corresponding value within the database

  Args:
      keyword (str): Text to be replcaced.

  Returns:
      Dict: Replaced value in following format. {'result':'[Replacement]'}
  """

  try:
    with open(file=replace_data_file, mode='r') as file:
      json_data = json.load(file)
    result =  json_data[keyword.lower()]
  # Check if data file exists
  except OSError as err:
    if err.errno == 2 and not debug_mode:
      lib.error_handling(f'Data file "{replace_data_file}" file does not exist')
    else:raise
  # Check if keyword exists
  except KeyError as err:
    message = f'Keyword "{keyword}" does not exist.'
    lib.error_handling(message, exit=False)
    return { 'error' : message }
  else:
    return { 'result' : result}

# Main routine to test the program in command line
if __name__ == '__main__':
  keyword = ''
  logger = lib.logging
  while keyword != 'q':
    keyword = input('Please Enter Keywod (q for exit) : ')
    if keyword != 'q':
      result = replace_function(keyword)
      logger.debug('End of Step')
      if 'result' in result:
        print(result)
    else:
      print('Exiting with "q" command.')
      logger.debug('End of Program')
 