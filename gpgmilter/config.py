
import logging

logger = logging.getLogger("gnupg-milter")
logging.basicConfig()

from logging import DEBUG, INFO, WARN, ERROR
loglevel = [DEBUG, INFO, WARN, ERROR]

class Config(object):
    '''
    A configuration for the gnupg-milter.
    '''

    # message to add to the email body (None for no appendend message)
    #TODO add warnings
    msg = """This mail has been automatically encrypted at your ISP."""

    # pipe file to use for message passign between sendmail and gnupg-milter
    socket = "unix:/var/spool/postfix/var/spool/gnupg-milter/milter.socket"

    # abort milter actions after no input for x seconds
    #FIXME is that so?
    timeout = 600

    # GPG home directory (where the key rings roam)
    #FIXME don't use temp!!!
    gnupghome = "/tmp/gpgmilter"

    def init_config(self, filename=None):
        '''
        Read the configuration file and store results in this
         object.
        If filename is None, the default configuration will 
        be used.
        '''
        #TODO read real config file
        return

    def log(self, msg, level=INFO):
        #TODO implement syslog
        #TODO static or per-object?
        assert level in loglevel, "Invalid logging level"
        print("BLA")
        logger.log(level, msg)

