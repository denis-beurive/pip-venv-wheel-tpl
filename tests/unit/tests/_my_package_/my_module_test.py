import unittest
import sys
import os
from my_package.my_module import return_ten


class TestMyModule(unittest.TestCase):

    __DIR__: str = ''
    __RESULT__: str = ''

    @classmethod
    def setUpClass(cls) -> None:
        TestMyModule.__DIR__ = os.path.dirname(os.path.abspath(__file__))
        TestMyModule.__RESULT__ = os.path.join(TestMyModule.__DIR__,
                                               os.path.pardir,
                                               os.path.pardir,
                                               'result')

    def test_return_ten(self):
        output_file = os.path.join(TestMyModule.__RESULT__, 'TestMyModule-test_return_ten')
        with open(output_file, 'w') as fd:
            fd.write('\n'.join(sys.path))
        self.assertEqual(10, return_ten())
