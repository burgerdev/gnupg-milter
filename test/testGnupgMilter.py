#!/usr/bin/env nosetests

import unittest
import tempfile
import shutil
import sys
import os

import Milter
import gnupg

# include the top directory in the search path, if the module is not yet added
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, "..")))

import gpgmilter


class TestGnupgMilter(unittest.TestCase):

    def setUp(self):
        with open("test.key", 'r') as keyfile:
            test_public_key = keyfile.read()

        # temp dir for keyrings, deleted in tearDown()
        self.d = tempfile.mkdtemp()

        # default config
        gpgm = gpgmilter.GnupgMilter()

        # import test key
        import_result = gpgm.gpgm_gpg.import_keys(test_public_key)
        assert import_result.count == 1
        self.fingerprint = import_result.fingerprints[0]

        self.gpgm = gpgm

    def tearDown(self):
        # remove temp dir
        shutil.rmtree(self.d)

    def testFingerprint(self):
        '''
        tests email-to-fingerprint functionality
        '''
        emails = ["test@example.com", "TEST@EXAMPLE.COM"]
        for email in emails:
            fp = self.gpgm.gpgm_get_public_key_fingerprint(email)
            self.assertEqual(fp, self.fingerprint,
                             msg="No fingerprint for <{}>".format(email))

    def testCanonicalize(self):
        emails = ['TEST@EXAMPLE.COM', '  \t test@example.COM \n\n']
        shouldBe = ['test@example.com', 'test@example.com']
        
        for pre, ref in zip(emails, shouldBe):
            post = self.gpgm.gpgm_canonical_email_address(pre)
            self.assertEqual(ref, post, msg="<{}> failed.".format(pre)) 

    def testFactory(self):
        teststr = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               "testdir"))
        conf = gpgmilter.config.Config()
        conf.gnupghome = teststr
        
        fac = gpgmilter.GnupgMilter.gpgm_get_factory(conf)
        obj = fac()
        self.assertEqual(obj.gpgm_gpg.gnupghome, teststr)




