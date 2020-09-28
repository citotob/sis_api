#from hashlib import md5
import hashlib
from base64 import b64decode
from base64 import b64encode
#from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Hash import MD5


# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
#pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    # Padding for the input string --not
    # related to encryption itself.
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        #self.key = hashlib.md5(key.encode('utf8')).hexdigest()
        self.key = key.encode("utf8")
        #self.key = hashlib.sha256(key.encode('utf8')).digest()

    def encrypt(self, raw):
        #raw = pad(raw.encode('utf8'), BLOCK_SIZE)
        raw = pad(raw.encode('utf8'))
        cipher = AES.new(self.key, AES.MODE_ECB)
        aa = cipher.encrypt(raw)
        return b64encode(aa)

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')

    def md5(self, raw):
        h = MD5.new()
        h.update(raw.encode("utf8"))
        return h.hexdigest()

##
# MAIN
# Just a test.
#msg = input('Message...: ')
#pwd = input('Password..: ')

#print('Ciphertext:', AESCipher("00077b93d83e4ff3a65014ac5ad64e2f").encrypt("agentKey=123&appKey=nb20180610&gamePlayerId=3700001&verifyStr=47c5aae67cae5cfb2866c7adf8e654b0"))
#print('CiphertextDecrypt:', AESCipher("00077b93d83e4ff3a65014ac5ad64e2f").decrypt("=0ezw9Lv5P9sEDbu+nZgEy/qx9Katj+ZiEecbs7YC+DWwFE34EFBpQiqK4FhSrpKR8goRdWVzJa8mVCiPqtB0SkHKxx0xquArPggRaASFRFObOtHhMEXmbAhz7mTuvwNbRiXoM+KCtqOYKEXB7RfQkH3yn3nknrmMvToqT2OTF9Q0wAJCrabf7D8jo30Qa7oZI/UEQECStl643weuDm+hQQ=="))