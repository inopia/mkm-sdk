from six.moves import urllib_parse

from .api import Api
from . import exceptions
from .serializer import XMLSerializer


class SimpleResolver(object):
    """

    """

    def __init__(self, sandbox_mode, auth_tokens={}, version='current'):
        self.url = ''
        self.method = ''
        self.api = Api(auth_tokens=auth_tokens, sandbox_mode=sandbox_mode, version=version)

    def setup(self, api_map=None, data=None, **kwargs):
        """
        Set up the url with required parameters and method of the request

        Params:
            `api_map`: Dict with urls and methods for the request
            `kwargs`: Optional additional parameters to be attached to the url
        """

        if api_map is None:
            raise Exception('Resolve must be called with `api_map` argument')
        elif api_map.get('url') is None or api_map.get('method') is None:
            raise Exception('Resolve must be called with a map with `url` and `method`')

        url = api_map['url']
        method = api_map['method']

        if method == "get" and type(data) is dict:
            params = api_map.get("params", [])
            for key in data.keys():
                assert key in params, "{key} is not parameter list {list}".format(key=key, list=params)

        # MKMAPI is weird like that
        if type(data) is dict:
            for key, value in data.items():
                if value in [True, False]:
                    data[key] = str(value).lower()

        try:
            url = url.format(**kwargs)
        except KeyError as param:
            raise exceptions.MissingParam(param=param)

        # We percent encode the url so that if any string has spaces,
        # commas or any other special character the url will be correctly formed anyway
        self.url = urllib_parse.quote(url)
        self.method = method

    def resolve(self, api_map=None, data=None, **kwargs):
        """
        Params:
            `api_map`: Dict with urls and methods for the request
            `data`: Data sent to MKM in PUT, POST and DELETE requests
            `kwargs`: Optional additional parameters to be attached to the url

        Return:
            `response`: Returns the response received from the server
        """
        self.setup(api_map=api_map, data=data, **kwargs)

        if isinstance(data, dict) and self.method is not 'get':
            serializer = XMLSerializer()
            data = serializer.serialize(data=data)

        if self.method == "get":
            return self.api.request(url=self.url, method=self.method, params=data)
        else:
            return self.api.request(url=self.url, method=self.method, data=data)
