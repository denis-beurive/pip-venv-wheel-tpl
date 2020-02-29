import setuptools
from typing import List, Generator, Pattern
import os
import re


# See: https://docs.python.org/3.6/distutils/setupscript.html
# WARNING: make sure to declare the file "data/description.md" as a "data file"
#          (see key "data_files").
__DIR__ = os.path.dirname(os.path.abspath(__file__))
long_description_path = os.path.join(__DIR__, 'data', 'description.md')

with open(long_description_path, "r") as fh:
    long_description = fh.read()

# Get the list of packages under the directory "lib".
#
# Please note that, since Python 3.3 the presence of the file "__init__.py" in
# the package directory is not mandatory anymore. See "Implicit Namespace
# Packages" at https://www.python.org/dev/peps/pep-0420/
#
# However, for "setuptools.find_packages()" to work, you must create a file
# called "__init__.py" in the package directory.
#
# See: https://setuptools.readthedocs.io/en/latest/setuptools.html
#
# If you use implicit namespace packages (since Python 3.3), then you can use
# the method "setuptools.find_namespace_packages()".

use_implicit_namespace_packages = False

src_dir = os.path.join(__DIR__, 'src')
if use_implicit_namespace_packages:
    # No package initializer "__init__.py" is required (since Python 3.3).
    packages_src = setuptools.find_namespace_packages(where=src_dir)
else:
    # Package initializers "__init__.py" are required.
    packages_src = setuptools.find_packages(where=src_dir)


# Load the requirements.
#
# Please note that the requirement files must be generated prior to this
# operation:
#
#    * pipenv lock --requirements > requirements.txt
#    * pipenv lock --requirements --dev > requirements-dev.txt
#
# See the sections "[dev-packages]" and "[packages]" of the "Pipfile".


def parse_requirements(filename: str) -> List[str]:
    """load requirements from a pip requirements file
    """
    keeper: Pattern = re.compile('^\\s*[^#\\-]')
    liner: Generator = (line.strip() for line in open(filename))
    return [line for line in liner if line and keeper.match(line) is not None]


requirements = parse_requirements(os.path.join(__DIR__, 'requirements.txt'))
requirements_dev = parse_requirements(os.path.join(__DIR__, 'requirements-dev.txt'))

print(requirements_dev)

setuptools.setup(
    author="Me",
    author_email="me@example.com",
    # The key "packages" lists the *names* of the packages. It does not list the
    # package directories. The paths to the directories are defined by the key
    # "package_dir".
    packages=packages_src,
    # See https://docs.python.org/3.6/distutils/setupscript.html#listing-whole-packages
    # Here, we say that all the package directories are located in the directory
    # "src". It is possible to assign specific directories for specific
    # packages.
    package_dir={'': 'src'},
    # Warning: you should avoid the use of the character "_" within the value of the parameter
    # "name". Although you could use the name "my_project", it would be converted into "my-project".
    name="my-project",
    version="0.1",
    description="My project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # See: https://docs.python.org/3.6/distutils/setupscript.html#installing-scripts
    # This key simply tells the installer that it must replace the path to the
    # interpreter after the "#!" (if present) by the path to the current
    # interpreter (or the one passed through the command line), in the
    # specified list of files.
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    # See: https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    # Once the package is installed, the console script "hello" will be
    # available. To see the list of all entry points for a given package you
    # can use the command bellow:
    #
    #    pip show <package name>
    entry_points={
        'console_scripts': ['hello = my_package.my_module:hello_world']
    },
    # Data files: files that must be included into the archive that is the
    # wheel.
    #
    # See: https://docs.python.org/3.6/distutils/setupscript.html#installing-additional-files
    #
    # Make sure to add all files used by the script "setup.py". In this case:
    # - requirements.txt
    # - requirements-dev.txt
    # - data/description.md
    #
    # "data_files" is an array of tuples. Each tuple contains 2 elements.
    # - The first element of the tuple (ex: "data") represents the target
    #   directory.
    # - The second element of the tuple (ex: "data/description.md") represents
    #   the file that will be copied into the distribution.
    data_files=[('', ['requirements.txt', 'requirements-dev.txt']),
                ('data', ['data/description.md'])],
    # List the requirements for the nominal/standard use of the distribution.
    # Related command:
    #
    #    pip install /path/to/sdist/dist.tar.gz
    install_requires=requirements,
    # List the requirements needed for optional/extra features.
    extras_require={
        'dev': requirements_dev
    }
)
