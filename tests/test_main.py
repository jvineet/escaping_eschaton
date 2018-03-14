#!/usr/bin/env python3.5

import unittest
import logging
from unittest.mock import MagicMock, patch
import os
import sys

SRCPATH = os.path.dirname(os.path.abspath(__file__))+'/..'
sys.path.append(SRCPATH)

import escape_eschaton as escape

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class SetupBasicTests(unittest.TestCase):
    """
        Sets up unit tests for basic helper routines inside lib
    """

    @classmethod
    def setUpClass(cls):
        cls.console = logging.StreamHandler(sys.stdout)
        cls.console.setLevel(logging.INFO)     
        logger.addHandler(cls.console)

        logger.info('Running unit tests for main routine ..')
        cls.json_chart1 = os.path.join(SRCPATH, 'tests', 'inputs', 'chart_test1.json')
        cls.json_chart2 = os.path.join(SRCPATH, 'tests', 'inputs', 'chart_test2.json')
        cls.json_chart3 = os.path.join(SRCPATH, 'tests', 'inputs', 'chart_test3.json')


    def test_solve(self):
        """
            Testing the routine that solves fpr the optimal escape path
        """
        mock_args = MagicMock()
        mock_args.chart = SetupBasicTests.json_chart1
        self.assertEqual(escape.solve(mock_args), [1,1,1])

        mock_args.chart = SetupBasicTests.json_chart2
        self.assertEqual(escape.solve(mock_args), [0,1,1,1,1])

        # testing for edge case when ther is no escape path
        mock_args.chart = SetupBasicTests.json_chart3
        self.assertEqual(escape.solve(mock_args), [])    
        

    @classmethod
    def tearDownClass(cls):
        logger.removeHandler(cls.console)


if __name__ == '__main__':
    unittest.main()