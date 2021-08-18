import logging, datetime, traceback, os, re, sys
from functools import wraps, partial
from timeit import default_timer as timer
from typing import Any, Optional, List, Dict, NoReturn

# Global Variables
debug_mode = False

# Default log parameters
log_params = {
  'folder' : 'log',
  'base_file_name' : 'pyapp.log',
  'level':logging.DEBUG,
  'format':'%(asctime)s:%(levelname)s:%(message)s',
  'encoding':'utf-8',
  'full_path_name':None,
  'clean':{'remove':True, 'days':0,'seconds':0, 'quantity':10}
}

def safe_run(func=None, **dkwargs):
  global debug_mode, log_params
  
  if func is None:
    return partial(safe_run, **dkwargs)

  # Initialize logging
  if 'log_params' in dkwargs and not log_params['full_path_name']:
    log_params = dkwargs['log_params']
    configure_logging(log_params)
  if 'debug_mode' in dkwargs:
    debug_mode = dkwargs['debug_mode']

  @wraps(func)
  def wrapper(*args, **kwargs):
    
    logging.debug(f'{func.__module__}.{func.__name__} function started with following paramaters: {args} {kwargs}')
    start = timer()
    if debug_mode:
      result = func(*args, **kwargs)
    else:
      try:
        result = func(*args, **kwargs)
      except Exception as err:
        error_handling(err)
    end = timer()
    process_time = '{:.2f}'.format((end - start) * 1000)
    logging.debug(f'{func.__module__}.{func.__name__} function ended in {process_time} milliseconds. returned {result}')
    return result

  return wrapper

# Error Handling
def error_handling(err, exit=True) -> Any:
  """Handles error object and writes the error into log file.

  Args:
      err ([type]): Error object.

  Returns:
      NoReturn: Exits Program.
  """

  global log_params
  traceback_string = traceback.format_exc()
  logging.error(str(err).replace('\n',' '))
  with open(log_params['full_path_name'], 'a') as file:
    file.write(f'{datetime.datetime.now()}\n{traceback_string}\n')
    print('Error:', err)
  if exit:
    sys.exit(1)
  else:
    return traceback_string

# Initialize and Configure Logging parameters.
def configure_logging(log_params_input:Dict=None) -> None:
  global log_params
  if log_params_input:
    log_params = log_params_input

  current_date_time = str(datetime.datetime.now()).replace(' ', '_')
  log_params['base_file_name'] = f'{current_date_time}.log'
  log_params['full_path_name'] = f'{log_params["folder"]}/{log_params["base_file_name"]}'
  log_file_handling(log_params=log_params)
  logging.basicConfig(format=log_params['format'], filename=log_params['full_path_name'] , encoding=log_params['encoding'], level=log_params['level'] )
  logging.debug(f'Logging initialized with following parameters: {log_params}')
  return logging

def log_file_handling(log_params:Dict) -> None:
  # Check if log folder exists
  log_folder_exists = os.path.exists(log_params['folder'])
  # Create folder if it does not exist
  if not log_folder_exists:
    os.makedirs(log_params['folder'])
  # Cleanup older logs
  files = os.listdir(log_params['folder'])
  
  while len(files) > log_params['clean']['quantity'] - 1 and len(files) > 0 and log_params['clean']['quantity'] >= 0:
    file_name = files[0]
    file_path = os.path.join(log_params['folder'], file_name)
    islog = re.search('\.log$', file_name)
    if islog:
      moddate = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
      curdate = datetime.datetime.now()
      diff = curdate - moddate
      days = diff.days
      seconds = diff.seconds
      # Clean older logs
      if log_params['clean']['remove'] and days >= log_params['clean']['days'] and \
        seconds >= log_params['clean']['seconds']:
        os.remove(file_path)
    files = os.listdir(log_params['folder'])
    
    
