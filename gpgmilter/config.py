
_KEY = """
PGPGPGPGPGPGPGPGPGPGPGPGPGP
"""

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
    gnupghome = "/tmp/gpg"
    

    @classmethod
    def init_config(cls, filename):
        '''
        read the configuration file and return a Config object
        '''
        #TODO read real config file
        return

