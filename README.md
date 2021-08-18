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
  * `Assignment.md` md version of Assignment text.
  * `Cloud Engineer Assignment TMNL August 21.pdf` Assignment text supplied by [TMNL](https://www.tmnl.nl/).
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
platform darwin -- Python 3.9.1, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /Users/leia/dev/tmnl/tmnl-app/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/leia/dev/tmnl/tmnl-app
collected 5 items                                                                                                                     

test/pytest/test_flaskapi.py::test_api_route PASSED                                                                             [ 20%]
test/pytest/test_flaskapi.py::test_authorization PASSED                                                                         [ 40%]
test/pytest/test_flaskapi.py::test_replacement PASSED                                                                           [ 60%]
test/pytest/test_flaskapi.py::test_key_error PASSED                                                                             [ 80%]
test/pytest/test_flaskapi.py::test_json_error PASSED                                                                            [100%]

========================================================== 5 passed in 0.38s ==========================================================
All Tests Passed Succesfully.
```


