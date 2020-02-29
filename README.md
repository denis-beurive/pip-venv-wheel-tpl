# Description

This repository contains a template for the development of a project using `pip` and `virtualenv`.
The present README file shows how to:

* setup a virtual environment.
* install the project in _editable/developer_ mode.
* generate the wheel.
* install the wheel with the default feature.
* install the wheel with an extra feature.
* getting information about the virtual environment and the installed package.
* using PyLint.
* write a scrip that executes the unit tests.
* organising the unit tests.

# Setup the virtual environment

Create the virtual environment and activate it:

    python -m virtualenv venv

Activate the virtual environment:

    REM Under MSDOS
    venv\Scripts\activate

    # Under Bash
    source venv\bin\activate

Get that last version of the tools `setuptools` and `wheel`:

    pip install --upgrade setuptools wheel

# Install the project in editable/developer mode

Get the source of the project:

    git clone git@github.com:denis-beurive/pip-venv-wheel-tpl.git

Install the distribution in _editable/developer_ mode:

    pip install -r requirements-dev.txt

Please note that:

* the option `-r` means: _install from the given requirements file_ (`requirements-dev.txt` in this case).
* the file `requirements-dev.txt` contains the following line: `-e .`. This line triggers the execution
  of the script `setup.py` in "_editable/developer_" mode.
* the file `requirements-dev.txt` contains the following line: `-r requirements.txt`. This line triggers the inclusion
  of the file `requirements.txt`.
* executing the script `setup.py` in "_editable/developer_" mode can also be done through these commands:
  * `python setup.py develop`
  * `pip install -e ./`

Test that the environment is well configured. The package `xmlrunner` should be installed and `PYTHONPATH` should point
to the directory `./src`.

    python -c "import xmlrunner"
    python -c "import sys; print(\"\n\".join([f\"{f}\" for f in sys.path]))"

> Please look at the section called "Get information about the installation" below.

# Running the unit tests
    
    python run_unittest.py --verbose

# Generate the wheel

    python setup.py sdist

# Install the wheel

There are two ways to install the wheel:

* you can install the wheel with the default features.
* you can install the wheel with extra features.

> Please note that there is no way to install a wheel in _editable/developer_ mode.
> The package (inside the wheel) will be installed as a dependency of your project (under the directory which path is
> given by the value of the environment variable `VIRTUAL_ENV`).

## Install the wheel with the default features

    pip install /path/to/dist/my_project-0.1.tar.gz

Test:

    python -c "import my_package.my_module"    
    hello

## Install the wheel with an extra feature (dev)

    pip install --find-links=/path/to/dist/my_project-0.1.tar.gz "my_project [dev]"

> Please note that, in our example, the extra feature called `dev` **has nothing to do with the _editable/developer_
> mode**.
> Edit the file `setup.py` and look at the following parameter: `extras_require={'dev': requirements_dev}`.
> An _extra feature_ only specifies the installation of extra packages.

## Get information about the installation

### Dependencies folder

If you wonder where the package has been installed, then you can execute the command below.

Under MSDOS:

    echo %VIRTUAL_ENV%

Under a UNIX shell:

    echo ${VIRTUAL_ENV}

### Get the list of installed dependencies

    > pip list

    Package           Version Location
    ----------------- ------- ----------------------------------------------------------
    args              0.1.0
    astroid           2.3.3
    clint             0.5.1
    colorama          0.4.1
    isort             4.3.21
    lazy-object-proxy 1.4.3
    mccabe            0.6.1
    my-project        0.1     c:\users\denis\desktop\test\pip-venv-tpl\src
    pip               19.3.1
    pylint            2.4.4
    setuptools        41.6.0
    six               1.13.0
    typed-ast         1.4.0
    wheel             0.33.6
    wrapt             1.11.2
    xmlrunner         1.7.7

Where does the name "`my-project`" come from ?

Short response: it comes from the file `setup.py`.

Long response: edit the code `setup.py`. You can see the code given below:

    setuptools.setup(
        ...
        name="my-project",
        ...
    )

> You should avoid the use of the character "_" within the value of the parameter "name".
> Although you could use the name "my_project", it would be converted into "my-project".

### Get information about an installed dependency

    pip show my-project

### Get the value of PYTHONPATH

    python -c "import sys; print(\"\n\".join([f\"{f}\" for f in sys.path]))"

# Running Pylint

    python -m pylint --rcfile=pylintrc src/

# Note about unit tests and naming collisions

Be aware that you must be very careful when you design your tests suite.

Please consider the code of the unit test runner [run_unittest.py](run_unittest.py):

    top_directory = os.path.join(__DIR__, 'tests', 'unit', 'tests')
    test_suite: TestSuite = defaultTestLoader.discover(start_dir=top_directory,
                                                       top_level_dir=top_directory,
                                                       pattern='*_test.py')
    print(f'Number of unit tests: {test_suite.countTestCases()}')
    result = xmlrunner.XMLTestRunner(output=target,
                                     verbosity=1,
                                     stream=terminal).run(test_suite)

* The parameter `start_dir` represents the top directory from which the test loader will search for test files.
  Test files end with "`_test.py`".
* The parameter `top_level_dir` represents the directory that marks the top of the packages namespace.

For example, let's consider the following directory tree:

    └───tests
        └───unit
            └───tests
                └───my_package
                    │   my_module_test.py

If we consider this code:

    top_directory = os.path.join(__DIR__, 'tests', 'unit', 'tests')
    test_suite: TestSuite = defaultTestLoader.discover(start_dir=top_directory,
                                                       top_level_dir=top_directory,
                                                       pattern='*_test.py')

The test loader searches for test files under the directory `tests/unit/tests`.
It will find one test file: `tests/unit/tests/my_package/my_module_test.py`.
And it will consider that this file is a (test) **module**: `my_package.my_module_test`.

Thus the test loader identifies a package called `my_package` under the directory `tests/unit/tests` !

But, keep in mind that there is a package with the same name (`my_package`) under the directory `src` !

Therefore, depending on the value of `PYTHONPATH`, one of the two packages is found:
`tests/unit/tests/my_package` or `src/my_package`.

Now, consider the code of `tests/unit/tests/my_package/my_module_test.py`:

    from my_package.my_module import return_ten
    ...

When the test file `tests/unit/tests/my_package/my_module_test.py` is run, you expect the package `src/my_package`
to be loaded (and not the package `tests/unit/tests/my_package`!).

But the test runner always insert the path to the test package at position 0 of `PYTHONPATH`.
Thus, the package `tests/unit/tests/my_package` will be loaded...

The module `my_package.my_module` won't be found since Python searches of a file `my_module.py` under
`tests/unit/tests/my_package`.
