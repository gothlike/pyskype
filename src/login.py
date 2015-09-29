import re, os, socket
from binascii import *
from things import *
from dh_rc4 import transport_stream
from rsa_aes import *
import rsa_keygen
from dump import dump_profile


class PyLogin(object):
    """

    """

    login_host = '91.190.216.17'
    login_port = 33033

    e = None
    n = None
    d = None
    cert = None

    skypename = None
    password = None

    def __init__(self, skypename, password):
        """

        :param skypename:
        :param password:
        :return:
        """
        self.skypename = skypename
        self.password = password

        self.e, self.n, self.d, self.cert = self._login_req()

    def _connect(self, host, port):
        """

        :param host:
        :param port:
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        return s

    def _encrypt(self, m):
        """

        :param m:
        :return:
        """
        return pow(m, self.e, self.n)

    def _decrypt(self, c):
        """

        :param c:
        :return:
        """
        return pow(c, self.d, self.n)

    def _n2m(self, n):
        """

        :param n:
        :return:
        """
        return unhexlify("%0256x" % n)

    def _m2n(self, m):
        """

        :param m:
        :return:
        """
        return int(hexlify(m), 16)

    def _rsa_pad(self, size, msg):
        """

        :param size:
        :param msg:
        :return:
        """
        msg = msg + sha1(msg).digest()
        pad = size - 3 - len(msg)  # pad the packet with 0xbb up to size bytes
        pkt = chr(0x4b) + (chr(0xbb) * pad) + chr(0xba) + msg + chr(0xbc)

        return pkt

    def _uic_pkt(self, nonce, salt):
        """

        :param nonce:
        :param salt:
        :return:
        """
        msg = sha1(self.cert + salt).digest() + salt + nonce

        return self._rsa_pad(0x80, msg)

    def _login_req(self):
        """

        :return:
        """
        e, n, d = rsa_keygen.make_rsa_keypair()

        print "Your private key: " + repr((e, n, d))

        s_stream = RsaAES(s=transport_stream(self._connect(self.login_host, self.login_port)),
                          skypename=self.skypename,
                          password=self.password)

        pub_key = unhexlify("%0256x" % n)

        login = [
            Buf(i=33, d=pub_key),
            Qword(i=49, d=unhexlify('2c097aeacabba291')),  # TODO: compute hostkey1
            Numbers(i=51, d=[0xcabba291, 0x9370a68d, 0xafcc1c6e, 0xe16fa568, 0xcabba291]),  # TODO: compute hostkey2
            String(i=13, d='2/4.3.0.37/172'),
            Dword(i=14, d=0x7f000001)
        ]

        response, params = s_stream.execute(0x000013a3, login)

        print response

        cert = getbyid(params, 36)[0].d

        dump_profile(cert)

        return e, n, d, cert

    def uic(self, nonce, salt):
        """

        :param nonce:
        :param salt:
        :return:
        """
        uic = unhexlify('00000104') + self.cert + self._n2m(self._decrypt(self._m2n(self._uic_pkt(nonce, salt))))

        return b2a_base64(uic)
