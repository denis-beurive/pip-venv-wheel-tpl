# This file illustrates the use of the module "unittest".
#
# Usage:
#
#          python run_unittest.py

import os
import sys
import argparse
from unittest import defaultTestLoader, TestSuite
from xmlrunner import xmlrunner
from tempfile import gettempdir


class Config:

    def __init__(self, verbose: bool):
        self._verbose = verbose

    @property
    def verbose(self) -> bool:
        return self._verbose


def main():

    __DIR__ = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description='Unit test runner')
    parser.add_argument('--verbose',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help=' '.join(['Verbosity mode']))
    args = parser.parse_args()
    try:
        conf = Config(args.__getattribute__('verbose'))
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    # target: path to the directory used to store the generated XML files.
    # terminal_path: path to the file used to store the standard output of the
    #                test execution.

    top_directory = os.path.join(__DIR__, 'tests', 'unit', 'tests')
    target = os.path.join(__DIR__, 'tests', 'unit', 'result')
    terminal_path = os.path.join(gettempdir(), 'terminal')

    if conf.verbose:
        print(f'XML files will be generated under the directory "{target}".')
        print(f'Path to the terminal file: "{terminal_path}".')

    with open(terminal_path, 'w') as terminal:
        test_suite: TestSuite = defaultTestLoader.discover(start_dir=top_directory,
                                                           top_level_dir=top_directory,
                                                           pattern='*_test.py')
        if conf.verbose:
            print(f'Number of unit tests: {test_suite.countTestCases()}')

        result = xmlrunner.XMLTestRunner(output=target,
                                         verbosity=1,
                                         stream=terminal).run(test_suite)

        # failure: a test that failed.
        # error: a Python related error.
        if len(result.failures) > 0 or len(result.errors) > 0:
            if conf.verbose:
                print(f'FAILURE (see file "{terminal_path}")')
            sys.exit(1)
        else:
            if conf.verbose:
                print('SUCCESS')
            sys.exit(0)


if __name__ == '__main__':
    main()
