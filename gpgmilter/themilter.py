
# python standard modules
import syslog
import StringIO

# python-milter modules
import Milter
from Milter.utils import parseaddr

# imports for this module
from gpgmilter import Config as config


class GnupgMilter(Milter.Base):

    gpgm_pk = None
    gpgm_me = "gnupg-milter"


    def __init__(self):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.

    @Milter.noreply
    def connect(self, IPname, family, hostaddr):
        '''
        incoming connection

        example parameters:
            IPname='mx.example.com', family=AF_INET, hostaddr=('23.5.4.3',4720)
            ..., family=AF_INET6, hostaddr=('3ffe:80e8:d8::1', 4720, 1, 0)
        '''
        self.gpgm_body = None
        self.log("connect from %s at %s" % (IPname, hostaddr))
        return Milter.CONTINUE

    def envfrom(self, mailfrom, *s):
        return Milter.CONTINUE

    @Milter.noreply
    def envrcpt(self, to, *s):
        toName, toAddr = parseaddr(to)
        self.gpgm_pk = self.gpgm_get_public_key_fingerprint(toAddr)
        if self.gpgm_pk is not None:
            self.log("Have private key for {}:\n{}".format(toAddr, self.gpgm_pk))
        else:
            self.log("No private key for {}.".format(toAddr))
        return Milter.CONTINUE

    @Milter.noreply
    def header(self, name, hval):
        return Milter.CONTINUE

    @Milter.noreply
    def eoh(self):
        self.gpgm_body = StringIO.StringIO()
        return Milter.CONTINUE

    @Milter.noreply
    def body(self, chunk):
        #TODO check if already encrypted
        self.gpgm_body.write(chunk)
        return Milter.CONTINUE

    def eom(self):
        if self.gpgm_pk:
            self.addheader("X-encrypted-by", self.gpgm_me)
        else:
            self.addheader("X-parsed-by", self.gpgm_me)
        self.gpgm_body.seek(0)
        self.log("The whole message:\n{}".format(self.fp.read()))
        if self.gpgm_pk:
            self.log("Crypted body:\n{]".format(self.gpgm_encrypt()))
        else:
            self.log("Not encrypting...")
        #TODO update body
        return Milter.ACCEPT

    def close(self):
        self.body.close()
        return Milter.CONTINUE

    def abort(self):
        # client disconnected prematurely
        return Milter.CONTINUE

  ## === Support Functions ===

    def log(self, *msg):
        logq.put((msg, self.id, time.time()))

    @staticmethod
    def canonical_email_address(addr):
        return addr.strip().lower()

    @classmethod
    def gpgm_get_public_key_fingerprint(cls, addr):
        def findKey(gpg, addr):
            for k in cls.gpgm_gpg.list_keys():
                for uid in k['uids']:
                    name, caddr = parseaddr(uid)
                    if cls.canonical_email_address(caddr) ==\
                            cls.canonical_email_address(addr):
                        print("Found fingerprint")
                        return k['fingerprint']
            return ""
    
    @classmethod
    def gpgm_encrypt(cls, data, fingerprint):
        assert isinstance(data, str), "Only strings can be encrypted."
        if len(str) == 0:
            return ""
        
        enc = cls.gpgm_gpg.encrypt(data, fingerprint)
        assert len(enc)>0, "Encryption failed."
        return enc

    @staticmethod
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

