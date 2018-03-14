"""
    setup script for installing the utilty
"""

import sys
from distutils.core import setup
from subprocess import Popen, PIPE


class TestFailureError(Exception):
    """
        Custom Exception; Raise when unit tests fail
    """
    def __init__(self, message):
       super().__init__(self, message)


# run unit_tests
def run_tests():
    """
        Run unit tets in a subprocess
    """
    python_executable = sys.executable
    cmd = [python_executable, '-m', 'unittest', 'discover', '-v']
    test_proc = Popen(cmd, stdout=PIPE,  stderr=PIPE)
    stdout_data, stderr_data = test_proc.communicate()
    if test_proc.returncode != 0:
        print(stderr_data.decode('utf-8'))
        raise TestFailureError("Unit test check failed")
    else:
        # print(stdout_data.decode('utf-8'))
        print(stderr_data.decode('utf-8'))


run_tests()

setup(name="escape_eschaton",
      version="0.1",
      description="Calculates most optimal path for escaping Eschaton Asteroid Field",
      author='Vineet Joshi',
      author_email='vineetjoshi006@gmail.com',
      scripts=['escape_eschaton.py'],
      packages = ['lib'],
      data_files=[('docs', ['docs/problem.pdf']),('./README.md')]
    )