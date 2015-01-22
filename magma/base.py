# -*- coding: UTF-8 -*-

from magma.session import Session
from magma.courses import CoursesList


class Student(object):
    """
    A student. This object is a higher-level wrapper for a session.
    """

    def __init__(self, year=None, firstname=None, lastname=None, passwd=None,
                 fetch=True, **kw):
        """
        Create a new student session. Unless you really know what you're doing
        you should pass ``year``, ``firstname``, ``lastname`` and ``passwd``
        arguments to let the module handle the login part.
        """
        self.session = Session(**kw)
        if year and firstname and lastname and passwd:
            self.session.login(year, firstname, lastname, passwd)
            if fetch:
                self.fetch()

    def fetch(self):
        """
        Fetch this student's courses page. It's recommended to do that when
        creating the object (this is the default) because the remote sessions
        are short.
        """
        soup = self.session.get_results_soup()
        self.courses = CoursesList(soup)
