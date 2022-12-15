import os
import base64
import hashlib
from Crypto.Cipher import DES3
from typing import AnyStr

import swype
from swype import http
from swype import gateways
from swype.exceptions import ConfigurationError

env = os.environ


class SwypeMeta(type):

    def __new__(mcs, *args, **kwargs):
        instance = super().__new__(mcs, *args, **kwargs)
        return mcs._configure_if_key(instance)

    @classmethod
    def _configure_if_key(mcs, instance):
        secret, public = env.get("secret_key"), env.get("public")
        if secret and public:
            instance.configure(secret, public, timeout=60)
        return instance


class Swype(metaclass=SwypeMeta):
    secret_key: AnyStr = None
    public_key: AnyStr = None
    timeout: int = None

    def __init__(self, secret_key: AnyStr, public_key: AnyStr, **kwargs):
        if public_key == "":
            raise ConfigurationError("Missing Public key")
        if secret_key == "":
            raise ConfigurationError("Missing Secret Key")
        self._secret_key = secret_key
        self._public_key = public_key
        self._timeout = kwargs.get("timeout", 60)

    @property
    def encryption_key(self):
        hashed = hashlib.md5(self._secret_key.encode("utf-8")).hexdigest()
        hashed_last12 = hashed[-12:]
        hashed_adjusted = self._secret_key.replace('FLWSECK-', '')
        hashed_first12 = hashed_adjusted[:12]
        # test the .encode('utf-8')
        return (hashed_first12 + hashed_last12).encode('utf-8')

    def encrypt(self, plaintext):
        blockSize = 8
        padDiff = blockSize - (len(plaintext) % blockSize)
        cipher = DES3.new(self.encryption_key, DES3.MODE_ECB)
        plaintext = "{}{}".format(plaintext, "".join(chr(padDiff) * padDiff))
        encrypted = base64.b64encode(cipher.encrypt(plaintext.encode('utf-8'))).decode('utf-8')
        return encrypted

    @classmethod
    def configure(cls, secret_key, public_key, **kwargs):
        cls.secret_key = secret_key
        cls.public_key = public_key
        cls.timeout = kwargs.get("timeout", 60)

    @classmethod
    def instantiate(cls):
        return cls(
            secret_key=cls.secret_key,
            public_key=cls.public_key,
            timeout=cls.timeout
        )

    @classmethod
    def gateway(cls):
        assert cls.secret_key and cls.public_key is not None, ConfigurationError(
            "Swype not configured."
            "API Keys not found in Environment variables."
            "Either set API Keys in environment variables or configure manually"
            " by calling 'Configuration.configure(secret_key='...', public_key='...', **kwargs)'"
        )
        return gateways.SwypeGateway(config=cls.instantiate())

    def _http(self):
        return http.Http(secret_key=self._secret_key, timeout=self._timeout)
