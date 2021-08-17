#!/bin/bash
# This script is designed to install, run and test a python module
# Written by Leia Renée
# Licence MIT
#
# Environment variables to be declared in .env
#
# PYTHONPATH=<pyrun_source_dir>:<pyrun_test_dir>:<other module folders if any>
# pyrun_venv_dir=<virtual env folder>
# pyrun_venv_python_version=<Python version>
# pyrun_source_dir=<source folder>
# pyrun_test_dir=<test folder>
# pyrun_python_module=<module name>
# pyrun_default_module_args=<module args>
# pyrun_test_wildcard=<Ex: test_*.py>
# pyrun_server_module=<server module>
# ----------------------------------------

# Stop on error
set -e

# Declare default variables
env_file=".env"

# Function for showing usage
function show_usage(){
  cat << EOF
  Script for easy running and testing '$pyrun_python_module' module
    Usage :
    - Install Virtual environment     $0 install
    - Run Tests:                      $0 test
    - Run Server:                     $0 server
    - Run Applicaiton                 $0 app
    - Show Usage:                     $0 help  
  
  To activate virtual environment for command line shell: (Not required for running '$0')
  - for 'bash, sh, ksh, csh, zsh...'
    '$pyrun_venv_dir/bin/activate'
  - for 'fish'
    '$pyrun_venv_dir/bin/activate.fish'
  
  To deactivate virtual environment:
    'deactivate'
EOF
  exit 0
}

# Function to import environment variables from .env file
function import_env_vars(){
  IFS=$'\n'
  # Declare environment varibles from .env file
  for env_var in $(cat $env_file)
  do
    export $env_var
  done
  IFS=$' '
}

# Function for preparing environment
function activate_virtual_env(){
  # Activate virtual environment
  if [ ! -d $pyrun_venv_dir ]
  then
    echo "Virtual environment is not installed. Run '$0 install' command first."
    exit 0
  else
    source $pyrun_venv_dir/bin/activate
  fi
  

}

# Function for running tests
function run_tests(){
  IFS=$'\n'
  tests=$(cd $pyrun_test_dir;ls $pyrun_test_wildcard | sed s/\.[^.]*$//g)
  echo "Following tests are found in $pyrun_test_dir with pattern $pyrun_test_wildcard"
  echo $tests
  echo
  for test in $tests
  do
    echo Running $test
    echo
    python3 -m unittest -v $test
    echo
  done
  IFS=$' '
}

# Function for calling python script with arguments
function run_application(){
  echo
  echo "Running $pyrun_python_module module "
  echo
 python3 -m $pyrun_python_module $@
}

# Function for running tests and python script at the same command.
function run_server(){
  echo
  echo "Running $pyrun_server_module Server "
  echo
  python3 -m $pyrun_server_module $@
}

function install(){
  echo
  echo "Installing virtual environment binaries into $pyrun_venv_dir with Python version $pyrun_venv_python_version"
  virtualenv -p $pyrun_venv_python_version $pyrun_venv_dir
  echo "Activating virtual environment"
  source "$pyrun_venv_dir/bin/activate"
  echo "Installing required packages"
  python3 -m pip install -r requirements.txt
  
}
# Main Routine

import_env_vars

if [ "$1" != "install"  ] && [ "$1" != "help" ]
then
  activate_virtual_env
fi

# Evaluate arguments and call sub functions
case $1 in
  "help")
  show_usage;;
  "test")
  run_tests;;
  "server")
  run_server;;
  "app")
  run_application;;
  "install")
  install;;
  *)
  run_application $@;;
esac





