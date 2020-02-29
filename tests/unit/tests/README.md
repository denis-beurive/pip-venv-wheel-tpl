


Be aware that you must be very careful when you configure the test suite.

    top_directory = os.path.join(__DIR__, 'tests', 'unit', 'tests')
    test_suite: TestSuite = defaultTestLoader.discover(start_dir=top_directory,
                                                       top_level_dir=top_directory,
                                                       pattern='*_test.py')
    print(f'Number of unit tests: {test_suite.countTestCases()}')
    result = xmlrunner.XMLTestRunner(output=target,
                                     verbosity=1,
                                     stream=terminal).run(test_suite)

* The parameter `start_dir` represents the top directory from which the test loader will search for test files.
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
And it will consider that this file is a (test) module: `my_package.my_module_test`.

Thus the test loader identifies a package called `my_package` under the directory `tests/unit/tests` !

But, keep in mind that there is a package with the same name (`my_package`) under the directory `src` !

Therefore, depending on the value of `PYTHONPATH`, one of the two packages is found:
`tests/unit/tests/my_package` or `src/my_package`.

When the test file `tests/unit/tests/my_package/my_module_test.py` is run, you expect the package `src/my_package`
to be loaded (and not the package `tests/unit/tests/my_package`!).

But the test runner always insert the path to the test package at position 0 of `PYTHONPATH`.
Thus, the package `tests/unit/tests/my_package` will be loaded...

Now, consider the code of `tests/unit/tests/my_package/my_module_test.py`:

    from my_package.my_module import return_ten
    ...

The module `my_package.my_module` won't be found since Python searches of a file `my_module.py` under
`tests/unit/tests/my_package`.
