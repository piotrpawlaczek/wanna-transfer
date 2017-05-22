"""Configuration module

Settings and defaults
"""
import os
import configparser


class Config(object):
    PARTNER_NAME = 'partner'
    ENCRYPTION_ALGORITHM = 'AES256'
    UPLOAD_PREFIX = 'in'
    BUCKET = 'mtp-cloudstorage'

    def __init__(self, vendor):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser('~/.wanna/credentials'))

        self.PARTNER_NAME = config.get('default', 'partner', fallback=self.PARTNER_NAME)
        self.ENCRYPTION_KEY = bytes(bytearray.fromhex(config.get('default', 'encryption_key', fallback='0000')))
        self.UPLOAD_PREFIX = config.get('default', 'upload_prefix', fallback='not-set')
        self.BUCKET = config.get('default', 'bucket', fallback=self.BUCKET)
        self.VENDOR = DATACENTERS[vendor.name.lower()](config)


class AWS(object):

    def __init__(self, cfg):
        self.API_KEY = cfg.get('aws', 'aws_access_key_id', fallback='missing')
        self.API_SECRET = cfg.get('aws', 'aws_secret_access_key', fallback='missing')


DATACENTERS = {
    'aws': AWS,
    'softlayer': NotImplementedError,
    'azure': NotImplementedError,
    'googlecloud': NotImplementedError
}
