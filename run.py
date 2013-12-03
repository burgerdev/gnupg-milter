#!/usr/bin/env python

import gpgmilter
import Milter
import gnupg

def main():

    #TODO parse command line

    # read configuration
    cfgfile = "/etc/gnupg-milter.conf"
    conf = gpgmilter.config.Config(cfgfile)
    conf.init_config(cfgfile)

    # Register to have the Milter factory create instances of your class:
    Milter.factory = gpgmilter.GnupgMilter.gpgm_get_factory(conf=conf)
    flags = Milter.CHGBODY + Milter.CHGHDRS + Milter.ADDHDRS
    flags += Milter.ADDRCPT
    flags += Milter.DELRCPT
    Milter.set_flags(flags)
    print("%s gnupg-milter startup" % time.strftime('%Y-%m-%d %H:%M:%S'))
    sys.stdout.flush()
    Milter.runmilter("gnupg-milter", config.socket, config.timeout)
    print("%s gnupg-milter shutdown" % time.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    main()

