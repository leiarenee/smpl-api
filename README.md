# Flask Api for Text Correction #

The purpose of this API is to correct specific words by finding and substituting them with corresponding phrases. Let's assume we have following substitution table.

| Search Key | Replacement    |
|------------|----------------|
| ABC        | ABC Co         |
| Rose       | Rose GMBH      |
| Frontier   | Frontier Lines |

Program will find literals such as `ABC`, `Abc`, `aBc.`, `/Abc` and other combinations, which might be composed of capital and lower case letters, only when the word is preceded and followed by a non letter character or space. Thereby keywords such as `ABCD`, `SABC` is neglected. Expressions matched by `regexp` is substituted with the respective keyword from the table.

## How it Works? ##

Following `Regexp` expression is used in order to provide a fast and comprehensive search and replace.

Search expression:

```regexp
(^|\W)([Aa][Bb][Cc])(\W|$)
```

Where `\W` expression stands for any non letter (characters other than a-z, A-Z, 0-9, including the _ (underscore) ) where it is logically `OR`'ed with start of the line (`^`) and end of the line (`$`). Capital and lower case string literals are extracted from `Search Key` for each character in the keyword to prepare a `[Aa][Bb][Cc]` like regular expression and iterated one by one over each item in the table in order to prepare a unique pattern specific to that keyword.
Replace expression:

```regexp
\1<replacement>\3
```

Since search expression has 3 capture groups, literals captured in these groups should be put back in replacement by using `\1` and `\3`.

Initially reverse replacement is executed to avoid replacing string literals that is already in replacements not to end up with `Àbc Co -> ABC ABC Co` like results, where search and replacement strings are interchanged .

## Pre-requisites ##

* Python 3.9 or later
* Pip
* Virtualenv
  
### Install ###

```sh
./pyrun.sh install
```

'pyrun.sh' is written in `bash` to easily install, test and run the module.

__Usage:__

* Install Virtual environment:    ./pyrun.sh install
* Run Tests:                      ./pyrun.sh test
* Run Server:                     ./pyrun.sh server
* Run Application:                ./pyrun.sh app
* Show Usage:                     ./pyrun.sh help
  
__Note:__
To activate virtual environment for command line shell: (Not required for running the module)

* bash, sh, ksh, csh, zsh and other sh compliant shells.
  
`$pyrun_venv_dir/bin/activate`

* fish
  
`$pyrun_venv_dir/bin/activate.fish`
  
To deactivate virtual environment:

`deactivate`

## Manual Install ##

* `cd [directory]`
* `virtualenv -p python3.9 venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

### Notes on manual install ###

* Do not change the `venv` virtual environment folder name.
* Use `source venv/bin/activate.fish` if you use fish shell

### Directory Structure ###

* `src` : Python source files
  * `replace.py` Main `Python3` source module.
  * `flaskapi.py` Flask backend web werver.
  * `library.py` Python module for helper functions, such as log handling, error handling, decorators.
* `test`: Folder for containing python unit, integration and system tests.
  * `test_replace.py` Python unit test file for `replace.py`
  * `files`: Folder including text and json files for testing purposes.
    * `test_input.txt` Sample input text file consumed by unit tests
    * `test_output.txt` Output text file used by unit test to compare results.
    * `test_replace_data.json` Json file used to extract sample data to be used in unit tests.
* `doc` : Extra documentation
* `log` : log files
* `venv` : virtual environment (This directory is created on first use by running `./pyrun.sh install`)
  * `bin` Virtual environment binaries
  * `lib` Python binaries and packages
* `root` :
  * `pyrun.sh` Helper bash script to run tests, install venv and run the python module.
  * `build-docker.sh` Bash script to build docker file locally.
  * `run-docker.sh` Bash script to run container locally.
  * `entrypoint.sh` Bash script used by Docker as entrypoint.
  * `README.md` This file
  * `requirements.txt` Used by pip to install required python packages.
  * `replace_data.json` Json file used to extract sample data from.
  * `.env` Environment varibles file
  * `gitignore` & `dockerignore` consumed by git and docker respectively to specify ignored files and folders.
  * `Dockerfile` Docker file used to build container image.
* `docker` Folder for extra docker files
  * `codebuild` Folder including AWS Codebuild files.
    * `codebuild.sh` Bash script to build to docker file remotly in AWS Codebuild.
    * `localbuild.sh` Bash script to test `codebuild.sh` locally.

## Run Tests ##

`./pyrun.sh test`

__Output:__

```sh
Starting tests

Running Unit Tests with python unittest library.
----------------------------------------------------------------------
Following tests are found in test/unittest with pattern unit_test_*.py
unit_test_replace

Running unit_test_replace

test_event_handler (unit_test_replace.Test_Replace) ... ok
test_load_data_file (unit_test_replace.Test_Replace) ... ok
test_neglect_inwords (unit_test_replace.Test_Replace) ... ok
test_reverse_replacement (unit_test_replace.Test_Replace) ... ok
test_several_replacements (unit_test_replace.Test_Replace) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.011s

OK


Running Integration tests with python pytest library.
========================================================= test session starts =========================================================
platform darwin -- Python 3.9.1, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /Users/leia/dev/smpl-api/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/leia/dev/smpl-api
collected 5 items                                                                                                                     

test/pytest/test_flaskapi.py::test_api_route PASSED                                                                             [ 20%]
test/pytest/test_flaskapi.py::test_authorization PASSED                                                                         [ 40%]
test/pytest/test_flaskapi.py::test_replacement PASSED                                                                           [ 60%]
test/pytest/test_flaskapi.py::test_key_error PASSED                                                                             [ 80%]
test/pytest/test_flaskapi.py::test_json_error PASSED                                                                            [100%]

========================================================== 5 passed in 0.38s ==========================================================
All Tests Passed Succesfully.
```

## Run Program from command line ##

Program supports running from the command line to test the api manually.

Run:

```bash
./pyrun.sh app
```

Enter the text that you want to paste and press enter to see the returning result. Press `q` to quit.

Output:

```bash
Running replace module 

Please Enter Keywod (q for exit) : The analysts of ABN did a great job!
The analysts of ABN Amro did a great job!
Please Enter Keywod (q for exit) : ABNormal
ABNormal
Please Enter Keywod (q for exit) : Abn amro, 
ABN Amro
Please Enter Keywod (q for exit) : TrioDos, volksBank, raboBank
Triodos Bank, de Volksbank, Rabobank
Please Enter Keywod (q for exit) : q
...
```

## Run the Api as a local server ##

```bash
./pyrun.sh server

Running flaskapi Server 

Server listens on 0.0.0.0:8000
 * Serving Flask app 'flaskapi' (lazy loading)
 * Environment: development
 * Debug mode: off

```

The Flask server starts to listen on `0.0.0.0:8000` by default. You can change these parameters in `.env` file using `HOST` and `PORT` environment variables.

Press `CTRL + C` to quit server.

## Test the Api Server Locally ##

Run:

```bash
./pyrun.sh server
```

Open another terminal then run the following command:

```bash
curl "http://0.0.0.0:8000/api/replace" -X POST -d '{"text" : "The analysts of ABN did a great job!"}' -H "Content-Type: application/json" -H "Authorization: Basic cmVwbGFjZTpyZXBsYWNl" 
```

Output:

```bash
curl "http://0.0.0.0:8000/api/replace" -X POST -d '{"text" : "The analysts of ABN did a great job!"}' -H "Content-Type: application/json" -H "Authorization: Basic cmVwbGFjZTpyZXBsYWNl" 
{"result":"The analysts of ABN Amro did a great job!"}
```

### About Flask API ###

Api endpoint : `/api/replace`
Request Method: POST

HTTP Basic Authentication is used in Flask Api server. Username and Password is `replace` and `replace` respectively. The base64 Encoding is `cmVwbGFjZTpyZXBsYWNl`.

Minimum Following headers should be sent in order to get a correct response:

* Content-Type: application/json
* Authorization: Basic cmVwbGFjZTpyZXBsYWNl

## Logging ##

Log files are created under `log` folder with timestamp as name.

Ex: `log/2021-08-18_18:09:41.342411.log`

Log parameters are setup in `log_params` global variable in `flaskapi.py` as follows:

```python
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
```

### Log Clean Up ####

Each execution creates a separate log file named with a timestamp. Clean up strategy is configured using `log_params['clean']` dictionary contents.

Ex:

```python
'clean':{'remove':True, 'days':7, 'seconds':0, 'quantity':-1} # Cleans up logs older than 1 week
'clean':{'remove':True, 'days':0, 'seconds':0, 'quantity':100} # Keeps Last 100 copies and removes the rest
'clean':{'remove':False, 'days':30, 'seconds':0, 'quantity':1000} # Disables clean up
```

### Safe Run Decorator & Tracing Slow Requests ###

Each function call is decorated with `lib.safe_run` decorator to achieve a standard mechanism to collect and log function execution times and errors.

Example Log Content:

```log
2021-08-18 18:23:38,839:DEBUG:Logging initialized with following parameters: {'folder': 'log', 'base_file_name': '2021-08-18_18:23:38.839197.log', 'level': 10, 'format': '%(asctime)s:%(levelname)s:%(message)s', 'encoding': 'utf-8', 'full_path_name': 'log/2021-08-18_18:23:38.839197.log', 'clean': {'remove': True, 'days': 0, 'seconds': 0, 'quantity': 1}}
2021-08-18 18:23:38,857:WARNING: * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
2021-08-18 18:23:38,858:INFO: * Running on http://192.168.8.190:8000/ (Press CTRL+C to quit)
2021-08-18 18:23:53,046:DEBUG:__main__.replaceapi function started with following paramaters: () {}
2021-08-18 18:23:53,046:DEBUG:"replace" Module Started.
2021-08-18 18:23:53,047:DEBUG:replace.replace_function function started with following paramaters: ('The analysts of ABN did a great job!',) {}
2021-08-18 18:23:53,051:DEBUG:replace.replace_function function ended in 4.14 milliseconds. returned {'result': 'The analysts of ABN Amro did a great job!'}
2021-08-18 18:23:53,051:DEBUG:End of "replace" Module main routine.
2021-08-18 18:23:53,051:INFO:Server HTTP 200 OK : {'result': 'The analysts of ABN Amro did a great job!'}
2021-08-18 18:23:53,051:DEBUG:__main__.replaceapi function ended in 5.07 milliseconds. returned <Response 55 bytes [200 OK]>
2021-08-18 18:23:53,057:INFO:127.0.0.1 - - [18/Aug/2021 18:23:53] "POST /api/replace HTTP/1.1" 200 -
2021-08-18 18:24:03,031:DEBUG:__main__.replaceapi function started with following paramaters: () {}
2021-08-18 18:24:03,031:ERROR:Server HTTP 400 Bad Request : "Text field must be specified"
2021-08-18 18:24:03,031:DEBUG:__main__.replaceapi function ended in 0.45 milliseconds. returned (<Response 41 bytes [200 OK]>, 400)
2021-08-18 18:24:03,032:INFO:127.0.0.1 - - [18/Aug/2021 18:24:03] "[31m[1mPOST /api/replace HTTP/1.1[0m" 400 -
```

`lib.safe_run` Decorator Function

```python
  # Decorator for generic error handling and logging.
  @staticmethod
  def safe_run(func=None, **dkwargs):
    global debug_mode
    if func is None:
      return partial(lib.safe_run, **dkwargs)

    @wraps(func)
    def wrapper(*args, **kwargs):
      
      logging.debug(f'{func.__name__} function started with following paramaters: {args} {kwargs}')
      start = timer()
      if debug_mode:
        result = func(*args, **kwargs)
      else:
        try:
          result = func(*args, **kwargs)
        except Exception as err:
          lib.error_handling(err)
      end = timer()
      process_time = '{:.2f}'.format((end - start) * 1000)
      logging.debug(f'{func.__name__} function ended in {process_time} milliseconds. returned {result}')
      return result

    return wrapper
```

Decorator accepts keyword arguments  in `dkwargs`. `functools.partial` function is used to support both parametric and non parametric decorator calls with `@` syntax. It executes the function in `try` block if `debug_mode` is `False` and runs it without `try`block if `debug_mode` is `True` in order to raise original exceptions to make debugging possible.
The other job of the decorator function call is to measure execution times and log it in the log file. This functionality can be helpful to trace slow requests when module is used as a part of backend api.

### About pyrun.sh and .env file ###

`pyrun.sh` is written for this application to easily run tests from command line. It looks for testing files that match a specified pattern within the testing directory. These parameters are supplied in `.env` file.

Contents of `.env` file

```sh
PYTHONPATH=src:test/unittest:test/pytest
pyrun_venv_dir=venv
pyrun_venv_python_version=python3.9
pyrun_source_dir=src
pyrun_unit_test_dir=test/unittest
pyrun_python_module=replace
pyrun_default_module_args=
pyrun_unit_test_wildcard=unit_test_*.py
pyrun_server_module=flaskapi
FLASK_APP=flaskapi.py
FLASK_ENV=development
FLASK_DEBUG=
HOST=0.0.0.0
PORT=8000
```

`pyrun.sh` is also used to install virtual environment in first use and run the python module activating virtual environment inside the script. Hence there is no need to activate the virtual environment if explicitly if the python module is run by `pyrun.sh`

## DOCKER ##

The application is ready to be installed as docker container. [Amazonlinux](https://gallery.ecr.aws/amazonlinux/amazonlinux) is used as a base image to keep stability and reliability. Since Docker Company puts quota downloading public images, using Docker hub public images from [AWS Codebuild](https://aws.amazon.com/codebuild/) is not reliable.

### Build Docker Image ###

Run:

```sh
./build-docker.sh
```

#### Manual Build Command ####

```sh
docker build . -t smpl-api --build-arg PYTHON_VERSION=3.9.5 --build-arg PYTHON_COMMAND=3.9
```

__Not__: Since `Python3.9` is not available as a yum package, source files are fetched from python.org ftp site, extracted, compiled and installed into container image during build time. Python version is passed into Docker Builder as an argument so that it can be changed easily from outside without changing docker file.

```docker
# STAGE 1: Build Stage - Build and Install python3
FROM public.ecr.aws/amazonlinux/amazonlinux AS python-builder
RUN yum update -y && yum groupinstall "Development Tools" -y
RUN yum install wget openssl-devel libffi-devel bzip2-devel -y
ARG PYTHON_VERSION
ARG PYTHON_COMMAND
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
 && tar xvf Python-${PYTHON_VERSION}.tgz
RUN cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations && make altinstall

# Install Python packages
WORKDIR /app
ADD requirements.txt .
RUN pip$PYTHON_COMMAND install -r requirements.txt

# Setup environment 
EXPOSE 8000
ENV PYTHONPATH=src
WORKDIR /app
ADD . .

# Set Entry Point command
ENTRYPOINT [ "./entrypoint.sh" ]
# Set Arguments
CMD [ "python3.9", "-m", "flaskapi" ]
```

`entrypoint.sh` is used as Docker entry point to be able to run extra commands and prepare environment before running server.

### Running Docker Container ###

Run:

```sh
./run-docker.sh
```

### Manual Run for docker container ###

Run:

```sh
docker run -p 8000:8000 smpl-api
```

### Running Tests in Docker Container ###

Run:

```sh
./run-docker.sh test
```

## AWS Codebuild for remote docker builds ##

[AWS Codebuild](https://aws.amazon.com/codebuild/) Service is used to build docker image remotely and deploy into [AWS Elastic Container Registry](https://aws.amazon.com/ecr/). `codebuild.sh` bash script file is executed codebuild machine. The settings are passed from [TG-Live](https://github.com/leiarenee/tg-live) github repository which is used by [Terragrunt](https://terragrunt.gruntwork.io/) and [Terraform](https://www.terraform.io/) to deploy infrastructure. See [TG-Live](https://github.com/leiarenee/tg-live) for more details.

### Local test for codebuild ###

`local-build.sh` under `docker/codebuild` folder is used to test `codebuild.sh` file locally.

Run:

```sh
docker/codebuild/local-build.sh
```

Following parameters are passed to `codebuild.sh` :

```sh
export APP_NAME=flask-api
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq .Account -r)
export IMAGE_REPO_NAME=$APP_NAME
export SOURCE_BRANCH=$(git branch | grep "*" | sed s/\*\ //g)
export DOCKER_FILE=./Dockerfile

export USE_REMOTE_DOCKER_CACHE=false 
export UPLOAD_IMAGE=false
export FETCH_AWS_SECRETS=false
export FETCH_REPO_VERSION=false
export ECR_LOGIN=$UPLOAD_IMAGE
export ECR_STATIC_LOGIN=false
export AWS_ECR_ACCOUNT_ID=

# Project ARGS
export PYTHON_VERSION=3.9.5
export PYTHON_COMMAND=3.9
```

__Note__: `aws` AWS Client application version > 2.0 and `jq` should be installed in order to run local-build.sh properly. AWS Credentials should be configured to upload resulting image. By default upload is disabled.

```sh
# Login to Elastic Container Registry
function ecr_login {
  echo -e "${GREEN}- Logging into ECR ${NC}"
  echo
  aws ecr get-login-password | docker login $ECR_URL -u AWS --password-stdin
  echo
}
```

### Remote Caching for Codebuild ###

While AWS Codebuild claims that it supports layer caching for docker images, it doesn't work smoothly most of the time. In order to overcome this problem remote caching is used. Latest image file from ECR is downloaded and used as a local cache for building docker image remotely. This mechanism makes build times multiple times faster than non cached builds.

### Secrets Handling for Docker builds ###

Secrets such as we use to access private repositories are stored in AWS Secrets service and fetched by `codebuild.sh` during build process.

```sh
# Fetch Secrets from secret manager
function fetch_secret {
  echo -e "${GREEN}- Feching Secret $1 from secret manager ${NC}";echo
  secret_value=$(aws secretsmanager get-secret-value --secret-id $2)
  echo "Successfully fetched $1";
  export $1=$(echo $secret_value | jq .SecretString | sed s/[\\]//g  | sed s/^\"//g | sed s/\}\"/\}/g )
}
```

### Future Releases ###

* System Tests
* Exception tests
* Get log parameters from configuration file
* `AWS Cloudwatch` logging

---

### Contact Information ###

Leia Renée

AWS Cloud Engineer

* Web : [renée.io](https://renée.io/)
* E-mail : [leiarenee20@gmail.com](mailto:leiarenee20@gmail.com)
* LinkedIn: [linkedin.com/in/leia-renee](https.//www.linkedin.com/in/leia-renee)
* Github : [github.com/leiarenee](https://github.com/leiarenee)
* Calendly: [calendly.com/leiarenee](https://calendly.com/leiarenee)
