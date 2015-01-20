# -*- coding: UTF-8 -*-

from session import Session
from courses import CoursesList

class Student(object):

    def __init__(self, year, firstname, lastname, passwd, fetch=True, **kw):
        self.session = Session(**kw)
        self.session.login(year, firstname, lastname, passwd)
        if fetch:
            self.fetch()


    def fetch(self):
        soup = self.session.get_soup("/~etudiant/inscriptions.php?quoi=1")
        self.courses = CoursesList(soup)
