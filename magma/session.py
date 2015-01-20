# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from requests import Session as BaseSession

try:
    from cookielib import LWPCookieJar
except ImportError:  # Python 3
    from http.cookiejar import LWPCookieJar

URLS = {
    'login': '/~etudiant/saisirMotDePasseEtudiant.php',
    'results': '/~etudiant/inscriptions.php?quoi=1',
}

DEFAULTS = {
    'user_agent': 'Python/P7Magma +b@ptistefontaine.fr',
    'base_url': 'magma.informatique.univ-paris-diderot.fr:2201',
}


class Session(BaseSession):
    """
    A session with builtin authentification support for Magma as well as custom
    default headers.

    This based on ``didelcli.session``:
        https://github.com/bfontaine/didelcli/blob/master/didel/session.py
    """

    def __init__(self, *args, **kwargs):
        """
        Same constructor as parent class but with a cookies jar.
        """
        user_agent = kwargs.pop('user_agent', DEFAULTS['user_agent'])
        base_url = 'http://' + kwargs.pop('base_url', DEFAULTS['base_url'])

        super(Session, self).__init__(*args, **kwargs)

        self.user_agent = user_agent
        self.base_url = base_url
        self.cookies = LWPCookieJar()


    def _set_header_defaults(self, kwargs):
        """
        Internal utility to set default headers on get/post requests.
        """
        headers = {'User-Agent': self.user_agent}
        req_headers = kwargs.pop('headers', {})
        headers.update(req_headers)
        kwargs['headers'] = headers


    def get_url(self, url):
        """
        Get the final URL for a given one. If it starts with a slash (``/``),
        the ``ROOT_URL`` is prepended.
        """
        if url.startswith('/'):
            url = '%s%s' % (self.base_url, url)
        return url


    def get(self, url, *args, **kwargs):
        self._set_header_defaults(kwargs)
        url = self.get_url(url)
        return super(Session, self).get(url, *args, **kwargs)


    def post(self, url, *args, **kwargs):
        self._set_header_defaults(kwargs)
        url = self.get_url(url)
        return super(Session, self).post(url, *args, **kwargs)


    def get_soup(self, *args, **kwargs):
        return BeautifulSoup(self.get(*args, **kwargs).text)

    def post_soup(self, *args, **kwargs):
        return BeautifulSoup(self.post(*args, **kwargs).text)


    def login(self, firstname, lastname, passwd):  # FIXME
        """
        Authenticate an user
        """
        url = URLS['login']
        params = {
            'prenom': firstname.upper(),
            'nom': lastname.upper(),
            'pwd': passwd,
        }

        soup = self.post_soup(url, params=params)

        return not soup.select('font[color=red]')  # errror
