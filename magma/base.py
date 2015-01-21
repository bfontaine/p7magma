# -*- coding: UTF-8 -*-

from magma.session import Session
from magma.courses import CoursesList

class Student(object):
    """
    A student. This object is a higher-level wrapper for a session.
    """

    def __init__(self, year, firstname, lastname, passwd, fetch=True, **kw):
        """
        Create a new student session.
        """
        self.session = Session(**kw)
        self.session.login(year, firstname, lastname, passwd)
        if fetch:
            self.fetch()


    def fetch(self):
        """
        Fetch this student's courses page. It's recommended to do that when
        creating the object (this is the default) because the remote sessions
        are short.
        """
        soup = self.session.get_soup("/~etudiant/inscriptions.php?quoi=1")
        self.courses = CoursesList(soup)
