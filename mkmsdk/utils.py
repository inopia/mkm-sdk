import base64
import csv
import gzip
import os
from io import StringIO
from . import exceptions


def _get_env_var(key):
    try:
        return os.environ[key]
    except KeyError:
        raise exceptions.MissingEnvVar(key)


def get_mkm_app_token():
    return _get_env_var('MKM_APP_TOKEN')


def get_mkm_app_secret():
    return _get_env_var('MKM_APP_SECRET')


def get_mkm_access_token():
    return _get_env_var('MKM_ACCESS_TOKEN')


def get_mkm_access_token_secret():
    return _get_env_var('MKM_ACCESS_TOKEN_SECRET')


def data_to_dictlist(b64data):
    """
    A few api endpoints return a base 64 encoded and gzipped csv file.
    This is a helper for decoding them into list of dicts
    """
    gzipped_buf = StringIO(base64.b64decode(b64data))
    csv_buf = StringIO(gzip.GzipFile(fileobj=gzipped_buf).read())
    data = list(csv.reader(csv_buf))

    gzipped_buf.close()
    csv_buf.close()

    header = data[0]
    return [zip(header, row) for row in data[1:]]
