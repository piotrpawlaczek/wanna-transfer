"""This module provides high level abstractions for efficient
download from the cloud. It handles several things for the user:

* Automatically switching to multipart transfers when
  a file is over a specific size threshold
* Uploading a file in parallel
* Progress callbacks to monitor transfers
* Retries. When possible.
"""
import difflib
import logging

LOG = logging.getLogger(__name__)


class IntegrityError(Exception):
    pass


def download_file(
        path, vendor, use_encryption=True, add_checksum=False, progress=False, prefix=None, ignore_prefix=False):
    """Download file from the cloud.

    Args:
        path (str): path to the file
        vendor (str): datacenter name: 'aws|softlayer|azure|googlecloud'
        use_encryption (bool): should the file be decrypted
        add_checksum (bool): should the control sum be checked
        progress (bool): should the transfer be monitored
        prefix (string): file prefix
        ignore_prefix (bool): ignore all prefixes

    Returns:
        obj - confirmation(s) from the vendor
    """
    from wanna import setup_vendor

    vendor = setup_vendor(vendor, use_encryption, ignore_prefix)

    if add_checksum:
        chck_path = path + vendor.hash_checksum
        vendor.download_file(chck_path, use_encryption=False)

    resp = vendor.download_file(path, progress=progress)

    if add_checksum:
        with open(chck_path, 'rb') as chck_file:
            control1 = chck_file.read().strip()
        control2 = vendor.get_checksum(path)

        if control1 != control2:
            error = 'File corrupted!\n'
            error += ''.join(difflib.unified_diff(control2, control1))
            raise IntegrityError(error)
        else:
            LOG.info('\nIntegrity check: OK')

    return resp
