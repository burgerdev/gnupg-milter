#!/usr/bin/env python

from gpgmilter import GnupgMilter, Config as config

def main():

    # read configuration
    cfgfile = "/etc/gnupg-milter.conf"
    config.init_config(cfgfile)

    # run log daemon
    bt = Process(target=GnupgMilter.background)
    bt.start()

    # Register to have the Milter factory create instances of your class:
    Milter.factory = GnupgMilter
    flags = Milter.CHGBODY + Milter.CHGHDRS + Milter.ADDHDRS
    flags += Milter.ADDRCPT
    flags += Milter.DELRCPT
    Milter.set_flags(flags)       # tell Sendmail which features we use
    print("%s gnupg-milter startup" % time.strftime('%Y-%m-%d %H:%M:%S'))
    sys.stdout.flush()
    Milter.runmilter("gnupg-milter", config.socket, config.timeout)

    # wait for logging daemon to exit
    logq.put(None)
    bt.join()
    print("%s gnupg-milter shutdown" % time.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    main()
