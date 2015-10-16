__author__ = 'Sean'

from Crypto.Cipher import AES
import base64
import config
"""
base64 is used for encoding, which means to put data in a specific format.
It is not to be confused with encryption, which is used for disguising data.
"""

class Encryptor:
    encoded = ""
    decoded = ""
    secret = config.SECRET
    block_size = 16
    """
    The block size for a cipher obj can be 16, 24 or 32 bytes (16 bytes matches 128 bits).
    """
    padding = '{'
    """
    Padding is used to ensure that your value is always equal to a multiple BLOCK_SIZE in length.
    It does not matter which character is used in the padding, but the universal preference is by using '{'.
    """
    def __init__(self):
        self.secret = config.SECRET
        """
        Imports the key that corresponds with this code.
        """

    def encrypt(self, private_info):
        pad = lambda s: s + (self.block_size - len(s) % self.block_size) * self.padding
        """
        This function is the actual process to pad the data being encrypted.
        Lambda is used for abstraction of functions. You must first define it,
        followed by the param, followed by a colon.
        Exemplary usage: addition = lambda x: x+5, therefore addition(3) = 8.
        """
        encode_aes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        """
        This function defines how the value gets encoded with the help of base64.
        AES is used for encryption.
        """

        cipher = AES.new(self.secret)
        """
        Creates the cipher obj using the key.
        """
        self.encoded = encode_aes(cipher, private_info)
        """
        Encodes the private_info that is placed within the encryption function.
        """

        return self.encoded

    def decrypt(self, encrypted_string):
        self.padding = '{'
        decode_aes = lambda c, e: c.decrypt(base64.b64decode(e)).decode("UTF-8").rstrip(self.padding)
        """
        This function defines how the value gets decoded with the help of base64.
        The .rstrip is used to strip away the PADDING from the encrypted value.
        Python does not recognize the function .rstip on its own and therefore needs
        the help of .decode("UTF-8") for it to work properly.
        """
        key = self.secret
        """
        The key is FROM the printout of 'secret' used in the encryption function.
        """
        cipher = AES.new(key)
        self.decoded = decode_aes(cipher, encrypted_string)

        return self.decoded
