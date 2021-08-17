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
  * `nginx_convert.py` Main `Python3` source module.
* `doc` : Extra documentation
  * `Assignment.md` Assignment text supplied by [Mendix](https://www.mendix.com/).
* `log` : log files
* `venv` : virtual environment (This directory is created on first use by running `./pyrun.sh install`)
  * `bin` Virtual environment binaries
  * `lib` Python binaries and packages
* `root` :
  * `pyrun.sh` Helper bash script to run tests, install venv and run the python module.
  * `input.yaml` Input source yaml file supplied by [Mendix](https://www.mendix.com/).
  * `nginx_conf.yaml` Configuration file to store python module defaults.
  * `nginx_conf` Sample Nginx Configuration file supplied by [Mendix](https://www.mendix.com/).
  * `README.md` This file
  * `requirements.txt` Used by pip to install required python packages. 

## Run Tests ##

`./pyrun.sh test`

__Output:__

```sh
Following tests are found in test with pattern test_*.py
test_nginx_conf test_nginx_out_conf test_parse_arguments

Running test_nginx_conf

test_create_file (test_nginx_conf.Test_Nginx_Configuration) ... Configuration file test/files/out/auto-test-out.conf created.
ok
test_load_input_file (test_nginx_conf.Test_Nginx_Configuration) ... ok
test_processed_input_data (test_nginx_conf.Test_Nginx_Configuration) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.045s

OK

Running test_nginx_out_conf

test_load_defaults (test_nginx_out_conf.Test_Nginx_Out_Conf) ... ok
test_output_file (test_nginx_out_conf.Test_Nginx_Out_Conf) ... ok
test_processed_inputs (test_nginx_out_conf.Test_Nginx_Out_Conf) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.033s

OK

Running test_parse_arguments

test_input_file_only (test_parse_arguments.Test_Nginx_Configuration) ... ok
test_print_app (test_parse_arguments.Test_Nginx_Configuration) ... ok
test_print_catchall (test_parse_arguments.Test_Nginx_Configuration) ... ok
test_print_ipfilters (test_parse_arguments.Test_Nginx_Configuration) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.052s

OK

```