# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from requests import Session as BaseSession

try:
    from cookielib import LWPCookieJar
except ImportError:  # Python 3
    from http.cookiejar import LWPCookieJar

URLS = {
    'login': '/~etudiant/controlerMotDePasseEtudiant.php',
    'logout': '/~etudiant/quitter.php',
    'results': {
        '2014_36': '/~etudiant/voirNotesM1.php',
        '2014_37': '/~etudiant/inscriptions.php?quoi=1',
    }
}

HEADERS = {
    'User-Agent': 'Python/P7Magma +b@ptistefontaine.fr',
}

DEFAULTS = {
    'base_url': 'magma.informatique.univ-paris-diderot.fr:2201',
}

YEARS = {
    "L3": "2014_1",
    "M1": "2014_36",
    "M2": "2014_37",
}


class Session(BaseSession):
    """
    A session with builtin authentification support for Magma

    This based on ``didelcli.session``:
        https://github.com/bfontaine/didelcli/blob/master/didel/session.py
    """

    def __init__(self, *args, **kwargs):
        """
        Same constructor as parent class but with a cookies jar.
        """
        base_url = kwargs.pop('base_url', DEFAULTS['base_url'])
        self.base_url = 'http://' + base_url
        headers = {}
        for k, v in HEADERS.items():
            headers[k] = kwargs.pop(k, v)

        super(Session, self).__init__(*args, **kwargs)
        self.headers.update(headers)
        self.cookies = LWPCookieJar()

    def get_url(self, url):
        """
        Get an absolute URL from a given one.
        """
        if url.startswith('/'):
            url = '%s%s' % (self.base_url, url)
        return url

    def get(self, url, *args, **kwargs):
        url = self.get_url(url)
        return super(Session, self).get(url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        url = self.get_url(url)
        return super(Session, self).post(url, *args, **kwargs)

    def get_soup(self, *args, **kwargs):
        """
        Shortcut for ``get`` which returns a ``BeautifulSoup`` element
        """
        return BeautifulSoup(self.get(*args, **kwargs).text)

    def post_soup(self, *args, **kwargs):
        """
        Shortcut for ``post`` which returns a ``BeautifulSoup`` element
        """
        return BeautifulSoup(self.post(*args, **kwargs).text)

    def get_results_soup(self, year=None):
        """
        ``get_soup`` on the results page. The page URL depends on the year.
        """
        if year is None:
            year = self.year
        year = YEARS.get(year, year)

        return self.get_soup(URLS['results'][year])

    def login(self, year, firstname, lastname, passwd, with_year=True):
        """
        Authenticate an user
        """
        firstname = firstname.upper()
        lastname = lastname.upper()

        if with_year and not self.set_year(year):
            return False

        url = URLS['login']
        params = {
            'prenom': firstname,
            'nom': lastname,
            'pwd': passwd,
        }

        soup = self.post_soup(url, data=params)

        return not soup.select('font[color=red]')  # error

    def logout(self):
        """
        Logout an user (untested)
        """
        self.get(URLS['logout'])

    def set_year(self, year):
        """
        Set an user's year. This is required on magma just before the login.
        It's called by default by ``login``.
        """
        self.year = YEARS.get(year, year)
        data = {'idCursus': self.year}
        soup = self.post_soup('/~etudiant/login.php', data=data)
        return bool(soup.select('ul.rMenu-hor'))
