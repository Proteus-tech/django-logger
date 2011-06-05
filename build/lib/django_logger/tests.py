import unittest
import logging
import os

import __init__ as logger

class TestLogger(unittest.TestCase):
    def test_LoggerClass(self):
        klass = logger.LoggerClass(
            default_level = logging.INFO,
            file_enabled = True,
            stream_enabled = True,
        )
        
        logging.setLoggerClass(klass)
        
        l = logging.getLogger('test')
        
        self.assertEqual(l.level, logging.INFO)
        self.assertEqual(l._meta.file_enabled, True)
        self.assertEqual(l._meta.stream_enabled, True)
