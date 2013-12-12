#!/usr/bin/env nosetests

import unittest
import sys
import os

# include the top directory in the search path, if the module is not yet added
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..")))

import gpgmilter

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testStorage(self):
        fn = os.path.abspath(os.path.join(current_dir, "..", "config", "gnupg-milter.conf"))
        conf = gpgmilter.config.Config(filename=fn)
        assert hasattr(conf, "gnupghome")
