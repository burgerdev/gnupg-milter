#!/usr/bin/env python

import Milter
import time
import email
import sys
from socket import AF_INET, AF_INET6
import StringIO
from Milter.utils import parse_addr

from multiprocessing import Process, Queue

logq = Queue(maxsize=4)


class myMilter(Milter.Base):

    def __init__(self):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.

    # each connection runs in its own thread and has its own myMilter
    # instance.  Python code must be thread safe.  This is trivial if only
    # stuff in myMilter instances is referenced.
    @Milter.noreply
    def connect(self, IPname, family, hostaddr):
    # (self, 'ip068.subnet71.example.com', AF_INET, ('215.183.71.68', 4720) )
    # (self, 'ip6.mxout.example.com', AF_INET6,
    #   ('3ffe:80e8:d8::1', 4720, 1, 0) )
        self.IP = hostaddr[0]
        self.port = hostaddr[1]
        if family == AF_INET6:
            self.flow = hostaddr[2]
            self.scope = hostaddr[3]
        else:
            self.flow = None
            self.scope = None
        self.IPname = IPname  # Name from a reverse IP lookup
        self.H = None
        self.fp = None
        self.receiver = self.getsymval('j')
        self.log("connect from %s at %s" % (IPname, hostaddr))

        return Milter.CONTINUE

    ##  def envfrom(self,f,*str):
    def envfrom(self, mailfrom, *str):
        self.F = mailfrom
        self.R = []  # list of recipients
        self.fromparms = Milter.dictfromlist(str)   # ESMTP parms
        self.user = self.getsymval('{auth_authen}')  # authenticated user
        self.log("mail from:", mailfrom, *str)
        self.fp = StringIO.StringIO()
        self.canon_from = '@'.join(parse_addr(mailfrom))
        self.fp.write('From %s %s\n' % (self.canon_from, time.ctime()))
        return Milter.CONTINUE

    ##  def envrcpt(self, to, *str):
    @Milter.noreply
    def envrcpt(self, to, *s):
        rcptinfo = to, Milter.dictfromlist(s)
        self.log(str(rcptinfo))
        self.R.append(rcptinfo)

        return Milter.CONTINUE

    @Milter.noreply
    def header(self, name, hval):
        self.fp.write("%s: %s\n" % (name, hval))
        return Milter.CONTINUE

    @Milter.noreply
    def eoh(self):
        self.fp.write("\n")
        return Milter.CONTINUE

    @Milter.noreply
    def body(self, chunk):
        self.fp.write(chunk)
        return Milter.CONTINUE

    def eom(self):
        self.fp.seek(0)
        msg = email.message_from_file(self.fp)
        # many milter functions can only be called from eom()
        # example of adding a Bcc:
        #self.addrcpt('<%s>' % 'spy@example.com')
        return Milter.ACCEPT

    def close(self):
        # always called, even when abort is called.  Clean up
        # any external resources here.
        return Milter.CONTINUE

    def abort(self):
        # client disconnected prematurely
        return Milter.CONTINUE

  ## === Support Functions ===

    def log(self, *msg):
        logq.put((msg, self.id, time.time()))


def background():
    while True:
        t = logq.get()
        if not t:
            break
        msg, id, ts = t
        print("%s [%d]" % (time.strftime('%Y%b%d %H:%M:%S',
                                         time.localtime(ts)), id))
        for i in msg:
            print(i)
        print("")


def main():
    bt = Process(target=background)
    bt.start()
    socketname = "unix:/var/spool/postfix/var/spool/gnupg-milter/milter.socket"
    timeout = 600
    # Register to have the Milter factory create instances of your class:
    Milter.factory = myMilter
    flags = Milter.CHGBODY + Milter.CHGHDRS + Milter.ADDHDRS
    flags += Milter.ADDRCPT
    flags += Milter.DELRCPT
    Milter.set_flags(flags)       # tell Sendmail which features we use
    print("%s milter startup" % time.strftime('%Y%b%d %H:%M:%S'))
    sys.stdout.flush()
    Milter.runmilter("pythonfilter", socketname, timeout)
    logq.put(None)
    bt.join()
    print("%s bms milter shutdown" % time.strftime('%Y%b%d %H:%M:%S'))

if __name__ == "__main__":
    main()
