from .api_map import _API_MAP as API_MAP
from . import resolvers

default_version = 'current'


class Mkm(object):

    def __init__(self, api_map=None, api_version=default_version, auth_tokens={}, **kwargs):
        """
        Initializes the api_map and eventual sandbox mode

        Params:
            `api_map`: Dict with urls and methods for the request
            `api_version`: Version of the api which should be used
            `kwargs`: Custom arguments that may specify if sandbox should be used

        """
        if api_map is None:
            self.api_map = API_MAP[api_version]['api']
        else:
            self.api_map = api_map

        self.api_version = api_version
        self.sandbox_mode = kwargs.get('sandbox_mode')
        self.auth_tokens = auth_tokens

    def __getattr__(self, name):
        """
        Used to get inside the api_map

        Params:
            `name`: api_map entry to get

        Returns:
            `instance`: Return an instance of Mkm with updated api_map
        """

        instance = Mkm(api_map=self.api_map[name], auth_tokens=self.auth_tokens, sandbox_mode=self.sandbox_mode, api_version=self.api_version)
        setattr(self, name, instance)
        return instance

    def __call__(self, *args, **kwargs):
        """
        Here is where the request happens

        Params:
            `kwargs`: May contain eventual parameters for the request

        Returns:
            `response`: Returns the response from the server
        """

        resolver = resolvers.SimpleResolver(self.sandbox_mode, self.auth_tokens, version=self.api_version)
        return resolver.resolve(api_map=self.api_map, **kwargs)

mkm = Mkm(api_map=API_MAP[default_version])
mkm_sandbox = Mkm(api_map=API_MAP[default_version], sandbox_mode=True)
