
import ConfigParser
import StringIO

import logging

logger = logging.getLogger("gnupg-milter")
logging.basicConfig()

from logging import DEBUG, INFO, WARN, ERROR
loglevel = [DEBUG, INFO, WARN, ERROR]

_defaults = {
    'message': """This mail has been automatically encrypted at your ISP.""",
    'socket': "unix:/var/spool/postfix/var/spool/gnupg-milter/milter.socket",
    'timeout': "600",
    'gnupghome': "",
    }

section = 'gnupg-milter'


class Config(object):
    '''
    A configuration for the gnupg-milter.
    '''
    
    def __init__(self, filename=None):
        '''
        Read the configuration file and store results in this
         object.
        If filename is None, the default configuration will 
        be used.
        '''

        self.parser = ConfigParser.SafeConfigParser(_defaults)
        self.parser.add_section(section)

        if filename is not None:
            self.parser.read([filename])
        
        for key in _defaults.keys():
            setattr(self, key, self.parser.get(section, key))

    def log(self, msg, level=INFO):
        #TODO implement syslog
        #TODO static or per-object?
        assert level in loglevel, "Invalid logging level"
        logger.log(level, msg)
    
    def __str__(self):
        s = StringIO.StringIO("")
        s.write("<{}.Config> object:\n".format(__name__))
        for attr in _defaults.keys():
            s.write("\t{} = {}\n".format(attr, getattr(self,attr)))
        return s.getvalue()

